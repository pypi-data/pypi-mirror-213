import logging
import json
import shlex
from subprocess import Popen, PIPE, CalledProcessError
from typing import Iterable, Dict, Any, List, Optional

logger = logging.getLogger(__name__)


def run_process_stream_result(command: str, env: Optional[Dict[str, str]] = None) -> Iterable[str]:
    """
    Run subprocess that streams stdout and stderr to handler functions
    :param command: the command line string to be executed
    :return: a generator of each returned line from STDOUT
    """
    with Popen(shlex.split(command), stdout=PIPE, stderr=PIPE, bufsize=1, universal_newlines=True, env=env) as p:
        for line in p.stdout:
            if line:
                yield line.encode('utf-8')
        err = p.stderr.read().encode('utf-8').decode()
    if p.returncode != 0:
        for line in err.split('\n'):
            logger.error(line)
        raise CalledProcessError(p.returncode, p.args, stderr=err)


def process_output_as_json(process_output: Iterable[str]) -> List[Dict[str, Any]]:
    """
    Convert the results of a subprocess to a json generator
    :param process_output: output from running `run_process(...)`
    :return:
    """
    return [json.loads(output) for output in process_output]


def run_process(command: str, env: Optional[Dict[str, str]] = None) -> List[str]:
    return list(run_process_stream_result(command, env))


def run_process_single_result(command: str, env: Optional[Dict[str, str]] = None) -> str:
    return run_process(command, env)[0]

