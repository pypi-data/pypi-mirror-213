"""Command line interface."""

import os
import sys
import importlib.util
from pathlib import Path

from .sbatch_function import load_func_call
from .pprint import pprint, pprint_info, pprint_error


def main():
    if len(sys.argv) < 2:
        pprint_error("Script path not provided.")
        pprint_info("Usage: py-sbatch-script FILENAME [script args]")
        sys.exit(1)

    script_file = Path(sys.argv[1])
    if not script_file.exists():
        pprint(f"<error>Script file does not exist</error>: '{str(script_file)}'.")
        pprint_info("Usage: py-sbatch-script FILENAME [script args]")
        sys.exit(1)

    # Delete the file from argv
    # so that script can use its own command line argument handling
    del sys.argv[1]

    script_file = script_file.resolve()
    script_dir = script_file.parent
    script_file = os.environ.setdefault("PY_SBATCH_SCRIPT_FILE", str(script_file))
    script_dir = os.environ.setdefault("PY_SBATCH_SCRIPT_DIR", str(script_dir))
    pprint(f"<info>Script file</info>: {str(script_file)}")
    pprint(f"<info>Script dir</info>: {str(script_dir)}")

    sys.path.append(script_dir)
    try:
        module_name = "_py_sbatch_script"
        spec = importlib.util.spec_from_file_location(module_name, script_file)
        module = importlib.util.module_from_spec(spec)  # type: ignore
        sys.modules[module_name] = module
        spec.loader.exec_module(module)  # type: ignore
    except Exception:
        raise RuntimeError("Failed to load module from script file")

    match load_func_call():
        case None:
            try:
                module.main()
            except Exception:
                raise RuntimeError("Call to main method in script file failed.")
        case {
            "func_name": func_name,
            "func_args": func_args,
            "func_kwargs": func_kwargs,
        }:
            try:
                sbatch_fn = getattr(module, func_name)
                sbatch_fn.func(*func_args, **func_kwargs)
            except Exception:
                raise RuntimeError("Calling saved function failed")
        case default:
            raise RuntimeError(f"Unexpected case {default}")
