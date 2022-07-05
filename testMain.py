"""
To run tests:
python -B ./testMain.py [suite1 ]...

To run test and coverage tool:
python -B -m coverage run ./testMain.py

To see coverage report on terminal:
python -m coverage report

To generate coverage lcov file:
python -m coverage lcov
"""

import datetime
import io
import os
import sys
import unittest
from typing import Dict, List, Set

import tests.logic.referee_unit as tlr_unit
import tests.test_suites as ts

_suites: Dict[ts.TestSuites, Set[unittest.TestCase]] = {}
# NOTE - gather tests from modules
_suites_list: List[Dict[ts.TestSuites, List[unittest.TestCase]]] = [
    tlr_unit.suites()
]
# NOTE - extend _suites with _suites_list
for d in _suites_list:
    for suite, tests in d.items():
        if suite not in _suites:
            _suites[suite] = set()
        _suites[suite].update(tests)


def main(argv):
    str_out = io.StringIO()
    runner = unittest.TextTestRunner(stream=str_out, verbosity=2)
    tests = unittest.TestSuite()
    desired_test_suites: Set[ts.TestSuites] = set()
    not_found_test_suites: Set[str] = set()
    # -----   -----
    for suite_name in argv:
        upper_name = suite_name.upper()
        try:
            desired_test_suites.add(ts.TestSuites[upper_name])
        except KeyError:
            not_found_test_suites.add(suite_name)
    str_suites_not_found = f"""{'+'*70}\nSUITE(S) NOT FOUND:\n{not_found_test_suites}\n{'-'*70}"""
    # -----   -----
    if len(desired_test_suites) == 0:
        for s in _suites:
            desired_test_suites.add(s)
    # -----   -----
    for dts in desired_test_suites:
        tests.addTests(_suites[dts])
    # NOTE - show suites not found on top of the generated test results file
    if len(not_found_test_suites) > 0:
        print(str_suites_not_found,'\n',file=str_out)
    result = runner.run(tests)
    # -----   -----
    time_now = datetime.datetime.now()
    file_name = time_now.strftime('%Y%m%d-%H%M%S')
    file_directory = './tests/output'
    if not os.path.isdir(file_directory):
        os.mkdir(file_directory)
    with open(file=f'{file_directory}/test-{file_name}.txt',
              mode='w', encoding='utf-8') as fp:
        print(str_out.getvalue(), file=fp)
    # -----   -----
    if len(not_found_test_suites) > 0:
        print(str_suites_not_found)
    if not result.wasSuccessful():
        print(f'Tests ran={result.testsRun} (failures={len(result.failures)+len(result.unexpectedSuccesses)}) (errors={len(result.errors)})')
    else:
        print('OK')

if __name__ == "__main__":
    main(sys.argv[1:])
