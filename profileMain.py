import argparse
import cProfile
import datetime
import io
import os
import pstats
import sys
import tracemalloc
from importlib import import_module

PKG_NAME = 'ESIIChess'


class ModuleArgs:
    cpu: bool = False
    mem: bool = False
    only_mine: bool = False
    input_module: str = ''
    output_path: str = ''


def _module_parser() -> argparse.ArgumentParser:
    prefix = '-'
    parser = argparse.ArgumentParser(
        description='Run python profilers on the main.py',
        prefix_chars=prefix)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(f'{prefix}c', f'{prefix*2}cpu',
                       dest='cpu', action='store_true',
                       help='Run cpu profiling')
    group.add_argument(f'{prefix}m', f'{prefix*2}mem',
                       dest='mem', action='store_true',
                       help='Run memory profiling')
    parser.add_argument(f'{prefix}o', f'{prefix*2}output',
                        dest='output_file',
                        help='File path to output the generated profiling text.')
    parser.add_argument(f'{prefix*2}mine',
                        dest='only_mine', action='store_true',
                        help=f'Measurements only to the package {PKG_NAME}')
    parser.add_argument('input_module',
                        help='A Python module, WITH a main, function to run the profiler on it. Module should be a string, like that on the statement: import module')
    return parser


def _parse_args(argv, parser: argparse.ArgumentParser):
    ma = ModuleArgs()
    namespace, others_args = parser.parse_known_args(
        argv, namespace=ma)  # type: ignore
    temp = os.path.normpath(namespace.input_module)
    temp = namespace.input_module.replace('.py', '')
    namespace.input_module = temp.replace(os.sep, '.')
    return namespace, others_args


_TIME_NOW = datetime.datetime.now()
_FILENAME_INFIX = _TIME_NOW.strftime('%Y%m%d-%H%M%S')
_FILE_DIRECTORY = './.profiling'


def _profile_output_path(module_args) -> str:
    if module_args.output_path != '':
        return module_args.output_path
    else:
        t = ''
        if module_args.cpu:
            t = 'cpu'
        elif module_args.mem:
            t = 'mem'
        return f'''{_FILE_DIRECTORY}/{t}-{_FILENAME_INFIX}.txt'''


def _profile_cpu(module, args, argv):
    # args are this module args
    # argv are the string arguments to the module beeing profiled
    cp = cProfile.Profile()
    str_out = io.StringIO()
    # SECTION - equivalent to: import module; cProfile.Profile().run(module.func())
    cp.enable()
    module.main(argv)
    cp.disable()
    # !SECTION - equivalent...
    # -----   -----
    # NOTE - treat results
    ps = pstats.Stats(cp, stream=str_out)
    ps.sort_stats(pstats.SortKey.CUMULATIVE)
    # ps.print_stats('^(?:(?!ESIIChess).)*$')  # NOTE - exclude with ESIIChess on path
    if args.only_mine:
        ps.print_stats(PKG_NAME)  # NOTE - show only with ESIIChess on path
    else:
        ps.print_stats()
    return str_out


def _profile_mem(module, args, argv):
    str_out = io.StringIO()
    tracemalloc.start(2)
    module.main(argv)
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()
    if args.only_mine:
        snapshot = snapshot.filter_traces(
            [tracemalloc.Filter(True, f'*{PKG_NAME}*')])
    stats = snapshot.statistics('lineno', cumulative=True)
    # stats = snapshot.statistics('filename')
    # stats = snapshot.statistics('traceback')
    for stat in stats:
        str_out.write(str(stat)+'\n')
    return str_out


def main(argv):
    args, other_args = _parse_args(argv, _module_parser())
    module = import_module(args.input_module)
    if not os.path.isdir(_FILE_DIRECTORY):
        os.mkdir(_FILE_DIRECTORY)
    str_out: io.StringIO = io.StringIO()
    # SECTION - cpu profiler
    if args.cpu:
        str_out = _profile_cpu(module, args, other_args)
    # !SECTION - cpu profiler
    # SECTION - memory profiler
    elif args.mem:
        str_out = _profile_mem(module, args, other_args)
    # !SECTION - memory profiler
    # NOTE - write profile to a file
    with open(file=_profile_output_path(args), mode='w', encoding='utf-8') as fp:
        print(str_out.getvalue(), file=fp)


if __name__ == '__main__':
    main(sys.argv[1:])
