from __future__ import annotations
import sys
import logging
from pathlib import Path
from subprocess import CompletedProcess, SubprocessError
from .colors import Colors


# Export root directory of the library
ZUT_ROOT = Path(__file__).parent


# Export typings from adequate library
if sys.version_info[0:2] < (3, 8):
    from typing_extensions import Literal, Protocol
else:
    from typing import Literal, Protocol
    
if sys.version_info[0:2] < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self


logger = logging.getLogger(__name__)


def is_list_or_tuple_of(instance, element_type: type|tuple[type]):
    if not isinstance(instance, (list,tuple)):
        return False

    for element in instance:
        if not isinstance(element, element_type):
            return False
        
    return True


def check_completed_subprocess(cp: CompletedProcess, logger: logging.Logger = None, *, label: str = None, level: int|str = None, accept_returncode: int|list[int]|bool = False, accept_stdout: bool = False, accept_stderr: bool = False, maxlen: int = 200):
    if not label:
        label = cp.args[0]

    if not logger and level is not None:
        logger = globals()["logger"]
    elif logger and level is None:
        level = logging.ERROR


    def is_returncode_issue(returncode: int):
        if accept_returncode is True:
            return False
        elif isinstance(accept_returncode, int):
            return returncode != accept_returncode
        elif isinstance(accept_returncode, (list,tuple)):
            return returncode not in accept_returncode
        else:
            return returncode != 0
    

    def extract_stream(content: str|bytes, name: str, color: str):
        if not isinstance(content, str):
            try:
                content = content.decode('utf-8')
            except UnicodeDecodeError:
                content = content.decode('cp1252')
        
        data = content.strip()
        if maxlen and len(data) > maxlen:
            data = data[0:maxlen] + '…'

        result = ''
        for line in data.splitlines():
            result += f"\n{color}[{label} {name}]{Colors.RESET} {line}"
        return result
    

    issue = False

    if is_returncode_issue(cp.returncode):
        message = f"{label} returned {Colors.YELLOW}code {cp.returncode}{Colors.RESET}"
        issue = True
    else:
        message = f"{label} returned {Colors.CYAN}code {cp.returncode}{Colors.RESET}"
    

    result = extract_stream(cp.stdout, 'stdout', Colors.CYAN if accept_stdout else Colors.YELLOW)
    if result:
        message += result
        if not accept_stdout:
            issue = True

    message += extract_stream(cp.stderr, 'stderr', Colors.CYAN if accept_stderr else Colors.YELLOW)
    if result:
        message += result
        if not accept_stderr:
            issue = True

    if issue:
        if logger:
            logger.log(level, message)
        else:
            raise SubprocessError(message)
    else:
        if logger:
            logger.log(logging.DEBUG, message)

    return issue


def get_venv() -> Path|None:
    """
    Return the path to the virtual environment if Python runs inside a virtual environment, None otherwise.
    """
    base_prefix = getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix
    if base_prefix == sys.prefix:
        return None
    return Path(sys.prefix)

