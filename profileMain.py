import argparse
import cProfile
import datetime
import io
import os
import pstats
import sys
import tracemalloc
from importlib import import_module


class ModuleArgs:
    cpu: bool = False
    mem: bool = False
    only_mine: bool = False
    input_module: str = ''


def _module_parser() -> argparse.ArgumentParser:
    prefix = '-'
    parser = argparse.ArgumentParser(
        description='Run python profilers on the main.py',
        prefix_chars=prefix)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(f'{prefix}c', f'{prefix*2}cpu',
                       dest='cpu', action='store_true',
                       help='')
    group.add_argument(f'{prefix}m', f'{prefix*2}mem',
                       dest='mem', action='store_true',
                       help='')
    parser.add_argument(f'{prefix*2}mine',
                        dest='only_mine', action='store_true',
                        help='')
    parser.add_argument('input_module',
                        help='A Python module, WITH a main, function to run the profiler on it. Module should be a string, like that on the statement: import module')
    return parser


def _parse_args(argv, parser: argparse.ArgumentParser):
    ma = ModuleArgs()
    return parser.parse_known_args(argv, namespace=ma)  # type: ignore


def main(argv):
    args, other_args = _parse_args(argv, _module_parser())
    module = import_module(args.input_module)
    cur_pkg = 'ESIIChess'
    time_now = datetime.datetime.now()
    file_name = time_now.strftime('%Y%m%d-%H%M%S')
    file_directory = './.profiling'
    if not os.path.isdir(file_directory):
        os.mkdir(file_directory)
    # SECTION - cpu profiler
    if args.cpu:
        cp = cProfile.Profile()
        # SECTION - equivalent to import module; cProfile.Profile().run(module.func())
        cp.enable()
        module.main(other_args)
        cp.disable()
        # !SECTION - equivalent...
        # -----   -----
        # NOTE - treat results
        str_out = io.StringIO()
        ps = pstats.Stats(cp, stream=str_out)
        ps.sort_stats(pstats.SortKey.CUMULATIVE)
        # ps.print_stats('^(?:(?!ESIIChess).)*$')  # NOTE - exclude with ESIIChess on path
        if args.only_mine:
            ps.print_stats(cur_pkg)  # NOTE - show only with ESIIChess on path
        else:
            ps.print_stats()
        fp = open(file=f'{file_directory}/cpu-{file_name}.txt',
                  mode='w', encoding='utf-8')
        print(str_out.getvalue(), file=fp)  # TODO - save on file
        fp.close()
    # !SECTION - cpu profiler
    # SECTION - memory profiler
    if args.mem:
        tracemalloc.start()
        module.main(other_args)
        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()
        if args.only_mine:
            snapshot = snapshot.filter_traces(
                [tracemalloc.Filter(True, f'*{cur_pkg}*')])
        stats = snapshot.statistics('lineno', cumulative=True)
        # stats = snapshot.statistics('filename')
        # stats = snapshot.statistics('traceback')
        fp = open(file=f'{file_directory}/mem-{file_name}.txt',
                  mode='w', encoding='utf-8')
        for stat in stats:
            print(stat, file=fp)
        fp.close()
    # !SECTION - memory profiler


if __name__ == '__main__':
    main(sys.argv[1:])
