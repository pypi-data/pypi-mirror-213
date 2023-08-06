"""
Job related helpers.
"""

from typing import Any, Callable, Dict, Generator, Optional, Union

import os
import json
import traceback
from aiohttp import ClientSession

import runpod.serverless.modules.logging as log
from .worker_state import IS_LOCAL_TEST, JOB_GET_URL
from .rp_tips import check_return_size


def _get_local() -> Optional[Dict[str, Any]]:
    """
    Returns contents of test_input.json.
    """
    if not os.path.exists("test_input.json"):
        log.warn("test_input.json not found, skipping local testing")
        return None

    with open("test_input.json", "r", encoding="UTF-8") as file:
        test_inputs = json.loads(file.read())

    if "id" not in test_inputs:
        test_inputs["id"] = "local_test"

    log.debug(f"Retrieved local job: {test_inputs}")
    return test_inputs


async def get_job(session: ClientSession, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Get the job from the queue.
    """
    next_job = None

    try:
        if config["rp_args"].get("test_input", None):
            log.warn("test_input set, using test_input as job input")
            next_job = config["rp_args"]["test_input"]
            next_job["id"] = "test_input_provided"
        elif IS_LOCAL_TEST:
            log.warn("RUNPOD_WEBHOOK_GET_JOB not set, switching to get_local")
            next_job = _get_local()
        else:
            async with session.get(JOB_GET_URL) as response:
                if response.status == 204:
                    log.debug("No content, no job to process.")
                    return None

                if response.status != 200:
                    log.error(f"Failed to get job, status code: {response.status}")
                    return None

                next_job = await response.json()
                log.debug(f"Received Job | {next_job}")

        if next_job.get("id", None) is None:
            log.error("Job has no id, unable to process.")
            next_job = None

        if next_job:
            log.debug(f"{next_job['id']} | Job Confirmed")
    except Exception as err:  # pylint: disable=broad-except
        log.error(f"Error while getting job: {err}")

    return next_job


def run_job(handler: Callable, job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run the job using the handler.
    Returns the job output or error.
    """
    log.info(f'{job["id"]} | Started')

    try:
        job_output = handler(job)
        log.debug(f'{job["id"]} | Handler output: {job_output}')

        run_result = {"output": job_output}

        if isinstance(job_output, dict):
            error = job_output.get("error", None)
            refresh_worker = job_output.get("refresh_worker", None)

            if error is not None:
                run_result = {"error": str(job_output["error"])}

            if refresh_worker is not None:
                job_output.pop("refresh_worker")
                run_result = {
                    "stopPod": True,
                    "output": job_output
                }

        elif isinstance(job_output, bool):
            run_result = {"output": job_output}

        check_return_size(run_result)  # Checks the size of the return body.
    except Exception as err:    # pylint: disable=broad-except
        log.error(f'Error while running job {job["id"]}: {err}')
        run_result = {"error": f"handler: {str(err)} \ntraceback: {traceback.format_exc()}"}
    finally:
        log.debug(f'{job["id"]} | Run result: {run_result}')

        return run_result  # pylint: disable=lost-exception


def run_job_generator(
        handler: Callable,
        job: Dict[str, Any]) -> Generator[Dict[str, Union[str, Any]], None, None]:
    '''
    Run generator job.
    '''
    try:
        job_output = handler(job)
        for output_partial in job_output:
            yield {"output": output_partial}
    except Exception as err:    # pylint: disable=broad-except
        log.error(f'Error while running job {job["id"]}: {err}')
        yield {"error": f"handler: {str(err)} \ntraceback: {traceback.format_exc()}"}
    finally:
        log.info(f'{job["id"]} | Finished ')

        return None  # pylint: disable=lost-exception
