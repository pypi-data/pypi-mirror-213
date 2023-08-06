"""Function runnable via sbatch."""

import os
import json
import shlex
from subprocess import CalledProcessError, run
from textwrap import dedent
from typing import Callable

from .pprint import pprint_error, pprint_info, pprint_cmd, pprint_json


def save_func_call(func_name, func_args, func_kwargs):
    func_call = dict(func_name=func_name, func_args=func_args, func_kwargs=func_kwargs)
    func_call_json = json.dumps(func_call)

    pprint_info("Saving function call:")
    pprint_json(func_call)
    os.environ["PY_SBATCH_SCRIPT_FUNC_CALL"] = func_call_json


def load_func_call():
    try:
        func_call_json = os.environ["PY_SBATCH_SCRIPT_FUNC_CALL"]
    except KeyError:
        return None

    func_call = json.loads(func_call_json)
    pprint_info("Loaded saved function call:")
    pprint_json(func_call)
    return func_call


class SbatchFunction:
    """Sbatch function wrapper."""

    def __init__(self, func: Callable):
        self.func = func

    def submit(self, sbatch_args: str, *func_args, **func_kwargs):
        save_func_call(self.func.__name__, func_args, func_kwargs)

        script_file = os.environ["PY_SBATCH_SCRIPT_FILE"]
        sbatch_args = dedent(sbatch_args).strip()
        sbatch_cmd = f"sbatch\n{sbatch_args}\n{script_file}"
        pprint_info("Submitting slurm job:")
        pprint_cmd(sbatch_cmd)

        cmd = shlex.split(sbatch_cmd)
        try:
            proc = run(cmd, text=True, check=True, capture_output=True)
            if proc.stdout is not None and proc.stdout.strip():
                print("Stdout:", proc.stdout)
            if proc.stderr is not None and proc.stderr.strip():
                print("Stderr:", proc.stderr)
            job_id = proc.stdout.strip().split()[-1]
            job_id = int(job_id)
            return job_id
        except CalledProcessError as e:
            pprint_error("Sbatch command submission failed")
            if e.stdout is not None and e.stdout.strip():
                print("Stdout:", e.stdout)
            if e.stderr is not None and e.stderr.strip():
                print("Stderr:", e.stderr)
            raise


def sbatch_function(func: Callable) -> SbatchFunction:
    return SbatchFunction(func)
