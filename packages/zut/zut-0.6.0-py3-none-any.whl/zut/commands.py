"""
Add and execute commands easily, based on argparse.
Usefull for non-Django applications.
For Django applications, use including command management instead.
"""
from __future__ import annotations
import logging, sys
from argparse import ArgumentParser, RawTextHelpFormatter, _SubParsersAction
from types import FunctionType, ModuleType
from pathlib import Path
from importlib import import_module
from importlib.util import find_spec
from .colors import Colors

logger = logging.getLogger(__name__)


def add_func_command(parser: ArgumentParser, func: FunctionType, add_arguments: FunctionType = None, name: str = None, doc: str = None):
    """
    Add the given function as a subcommand of the parser.
    """
    if name is None:
        name = func.__name__
    if doc is None:
        doc = func.__doc__

    subparsers = get_subparsers(parser)
    cmdparser: ArgumentParser = subparsers.add_parser(name, help=get_help_text(doc), description=get_description_text(doc), formatter_class=RawTextHelpFormatter)
    cmdparser.set_defaults(func=func)

    if add_arguments:
        add_arguments(cmdparser)

    return cmdparser


def add_module_command(parser: ArgumentParser, module: str|ModuleType, name: str = None, doc: str = None):
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


def add_package_commands(parser: ArgumentParser, package: str):
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


def get_subparsers(parser: ArgumentParser) -> _SubParsersAction:
    """
    Get or create the subparsers object associated with the given parser.
    """
    if isinstance(parser, _SubParsersAction):
        return parser
    elif parser._subparsers is not None:
        return next(filter(lambda action: isinstance(action, _SubParsersAction), parser._subparsers._actions))
    else:
        return parser.add_subparsers()


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


def run_command(parser: ArgumentParser, *args, default_func: FunctionType = None, default_add_arguments: FunctionType = None):
    """
    Run the command-line application, returning command result.
    """    
    func_args, unknown = parser.parse_known_args(*args)
    func_args = vars(func_args)
    func = func_args.pop('func', None)

    if func:
        if unknown:
            parser.print_usage(file=sys.stderr)
            print(f"{parser.prog}: error: unrecognized arguments: {' '.join(unknown)}", file=sys.stderr)
            return 2

    elif default_func:
        default_parser = ArgumentParser(prog=f"{parser.prog} (default)", formatter_class=RawTextHelpFormatter)

        if default_add_arguments:
            default_add_arguments(default_parser)

        func_args = vars(default_parser.parse_args(*args))
        func = default_func

    else:
        print(f"{Colors.RED}missing command name{Colors.RESET}", file=sys.stderr)
        return 2

    try:
        return func(**func_args)
    except KeyboardInterrupt:
        logging.getLogger(__name__).error("interrupted")
        return 1


def exec_command(parser: ArgumentParser, *args, default_func: FunctionType = None, default_add_arguments: FunctionType = None):
    """
    Run the command-line application and exit with appropriate return code.
    """
    r = run_command(*args, parser=parser, default_func=default_func, default_add_arguments=default_add_arguments)

    if not isinstance(r, int):
        r = 0 if r is None or r is True else 1
    exit(r)
