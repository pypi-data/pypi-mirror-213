"""
Add and execute commands easily, based on argparse.
Usefull for non-Django applications.
For Django applications, use including command management instead.
"""
from __future__ import annotations
import logging
import sys
from argparse import ArgumentParser, RawTextHelpFormatter, _SubParsersAction
from types import FunctionType, ModuleType
from pathlib import Path
from importlib import import_module
from importlib.util import find_spec
from typing import Any
from .process import get_exit_code

logger = logging.getLogger(__name__)


def create_command_parser(prog: str = None, version: str = None, description: str = None):
    parser = ArgumentParser(prog=prog, description=description, formatter_class=RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=f"%(prog)s {version if version else ''}")
    return parser


def add_func_command(parser: ArgumentParser|_SubParsersAction, func: FunctionType, add_arguments: FunctionType = None, name: str = None, doc: str = None):
    """
    Add the given function as a subcommand of the parser.
    """
    if name is None:
        name = func.__name__
    if doc is None:
        doc = func.__doc__

    subparsers = get_commands_subparsers(parser)
    cmdparser: ArgumentParser = subparsers.add_parser(name, help=get_help_text(doc), description=get_description_text(doc), formatter_class=RawTextHelpFormatter)
    cmdparser.set_defaults(func=func)

    if add_arguments:
        add_arguments(cmdparser)

    return cmdparser


def add_module_command(parser: ArgumentParser|_SubParsersAction, module: str|ModuleType, name: str = None, doc: str = None):
    """
    Add the given module as a subcommand of the parser.
    
    The command function must be named `handler` and the arguments definition function, if any, must be named `add_arguments`.
    """
    if not isinstance(module, ModuleType):
        module = import_module(module)

    func = getattr(module, 'handle')

    if name is None:
        name = module.__name__.split(".")[-1]
        if name.endswith('cmd') and len(name) > len('cmd'):
            name = name[0:-len('cmd')]
    
    add_arguments = getattr(module, 'add_arguments', None)
    add_func_command(parser, func, add_arguments=add_arguments, name=name, doc=doc)


def add_package_commands(parser: ArgumentParser|_SubParsersAction, package: str):
    """
    Add all modules in the given package as subcommands of the parser.
    """
    package_spec = find_spec(package)
    if not package_spec:
        raise KeyError(f"package not found: {package}")
    if not package_spec.origin:
        raise KeyError(f"not a package: {package} (did you forget __init__.py ?)")
    package_path = Path(package_spec.origin).parent
    
    for module_path in package_path.iterdir():
        if module_path.is_dir() or module_path.name.startswith("_") or not module_path.name.endswith(".py"):
            continue

        module = module_path.stem
        add_module_command(parser, f"{package}.{module}")


def get_commands_subparsers(parser: ArgumentParser) -> _SubParsersAction:
    """
    Get or create the subparsers object associated with the given parser.
    """
    if isinstance(parser, _SubParsersAction):
        return parser
    elif parser._subparsers is not None:
        return next(filter(lambda action: isinstance(action, _SubParsersAction), parser._subparsers._actions))
    else:
        return parser.add_subparsers(title='commands')


def get_help_text(docstring: str):
    if docstring is None:
        return None
    
    docstring = docstring.strip()
    try:
        return docstring[0:docstring.index('\n')].strip()
    except:
        return docstring


def get_description_text(docstring: str):
    if docstring is None:
        return None
    
    description = None
    indent_size = 0
    
    for line in docstring.splitlines(keepends=False):
        if description:
            description += '\n' + line[indent_size:]
        else:
            indent_size = 0
            for char in line:
                if char not in [' ', '\t']:
                    description = line[indent_size:]
                    break
                else:
                    indent_size += 1

    return description


def _get_default_name(parser: ArgumentParser, default: FunctionType):
    subparsers = get_commands_subparsers(parser)
    for name, subparser in subparsers.choices.items():
        if not isinstance(subparser, ArgumentParser):
            continue
        if subparser.get_default('func') == default:
            return name

    # not found: we add it    
    add_func_command(subparsers, default)
    return default.__name__


def get_command_func(parser: ArgumentParser, default: str|FunctionType = None, args: list[str] = None) -> tuple[FunctionType|int,dict[str,Any]]:
    """
    Run the command-line application, returning command result.
    """
    try:
        namespace, unknown = parser.parse_known_args(args)
    except SystemExit as e: # catch exit in case of --help or --version
        return e.code, {}

    kwargs = vars(namespace)
    func = kwargs.pop('func', None)

    if func:
        if unknown:
            logger.error(f"{parser.prog}: unrecognized arguments: {' '.join(unknown)}")
            return 2, {}

    elif default:
        # call get_command_func again, adding default at start of unknown arguments
        if not isinstance(default, str):
            default = _get_default_name(parser, default)

        if args is None:
            args = sys.argv[1:]
        new_args = args[:len(args)-len(unknown)] + [default] + unknown
        return get_command_func(parser=parser, args=new_args)

    else:
        logger.error(f"{parser.prog}: missing command name")
        return 2, {}
    
    return func, kwargs


def run_command_func(func: FunctionType|int, **kwargs):
    if isinstance(func, int):
        return func
    
    try:
        return func(**kwargs)
    except KeyboardInterrupt:
        logger.error("interrupted")
        return 1


def exec_command_func(func: FunctionType|int, **kwargs):
    r = run_command_func(func, **kwargs)
    r = get_exit_code(r)
    exit(r)


def run_command_parser(parser: ArgumentParser, default: str|FunctionType = None, args: list[str] = None):
    func, kwargs = get_command_func(parser=parser, default=default, args=args)
    return run_command_func(func, **kwargs)


def exec_command_parser(parser: ArgumentParser, default: str|FunctionType = None, args: list[str] = None):
    """
    Run the command-line application and exit with appropriate return code.
    """
    func, kwargs = get_command_func(parser=parser, default=default, args=args)
    exec_command_func(func, **kwargs)
