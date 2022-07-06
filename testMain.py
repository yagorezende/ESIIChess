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
from typing import Any, Dict, List, Sequence, Set

import tests.unit.logic.referee as tlr_unit
import tests.integ.logic.referee as tlr_integ
import tests.test_suites as ts

def _merge_dicts(dict1: Dict,dict2: Dict) -> Dict[Any,Set]:
    d: Dict[Any,Set] = {}
    for k,v in dict1.items():
        if k not in d:
            d[k] = set()
        d[k].update(v)
    for k,v in dict2.items():
        if k not in d:
            d[k] = set()
        d[k].update(v)
    return d


def print_test_result(result: unittest.TestResult):
    if result.wasSuccessful():
        print('OK')
    else:
        print(f'FAILED [Tests ran={result.testsRun} (failures={len(result.failures)+len(result.unexpectedSuccesses)}, errors={len(result.errors)})]')


_suites_unit_test: Dict[ts.TestSuites, Set[unittest.TestCase]] = {}
_suites_unit_test = \
    _merge_dicts(_suites_unit_test,tlr_unit.suites())

_suites_integ_test: Dict[ts.TestSuites, Set[unittest.TestCase]] = {}
_suites_integ_test = \
    _merge_dicts(_suites_integ_test,tlr_integ.suites())



def main(argv):
    str_out = io.StringIO()
    runner = unittest.TextTestRunner(stream=str_out, verbosity=2)
    desired_test_suites: Set[ts.TestSuites] = set()
    not_found_test_suites: Set[str] = set()
    # -----   -----
    # NOTE - get tests to run
    for suite_name in argv:
        upper_name = suite_name.upper()
        try:
            desired_test_suites.add(ts.TestSuites[upper_name])
        except KeyError:
            not_found_test_suites.add(suite_name)
    str_suites_not_found = f"""{'+'*70}\nSUITE(S) NOT FOUND:\n{not_found_test_suites}\n{'-'*70}"""
    # NOTE - get all tests if no one was defined
    if len(desired_test_suites) == 0:
        for s in _suites_unit_test:
            desired_test_suites.add(s)
    # -----   -----
    # NOTE - generate the output file
    time_now = datetime.datetime.now()
    file_name = time_now.strftime('%Y%m%d-%H%M%S')
    file_directory = './tests/output'
    if not os.path.isdir(file_directory):
        os.mkdir(file_directory)
    # -----   -----
    # NOTE - show suites not found on top of the generated test results file
    if len(not_found_test_suites) > 0:
        print(str_suites_not_found,'\n',file=str_out)
    # -----   -----
    proceed = True
    # SECTION - run smoke testing if needed
    if ts.TestSuites.SMOKE_TESTING in desired_test_suites:
        prompt = f'Running {ts.TestSuites.SMOKE_TESTING.name} suite:'
        print('+'*70)
        print('+'*70,file=str_out)
        print(prompt)
        print(f'{prompt}',file=str_out)
        dts = ts.TestSuites.SMOKE_TESTING
        desired_test_suites.remove(dts)
        tests = unittest.TestSuite(_suites_unit_test[dts])
        print(f'    {dts.name}... ', end='')
        result = runner.run(tests)
        print_test_result(result)
        if not result.wasSuccessful():
            proceed = False
        print('+'*70,file=str_out)
    # !SECTION - run smoke testing if needed
    # SECTION - run unit tests
    print('+'*70)
    print('+'*70,file=str_out)
    if not proceed:
        prompt = 'Skipping unit test suites.'
        print(prompt)
        print(f'{prompt}',file=str_out)
    else:
        prompt = 'Running unit test suites:'
        print(prompt)
        print(f'{prompt}',file=str_out)
        unit_tests_available = _suites_unit_test.keys()
        for dts in desired_test_suites:
            if dts not in unit_tests_available:
                continue
            tests = unittest.TestSuite()
            tests.addTests(_suites_unit_test[dts])
            print(f'    {dts.name}... ', end='')
            print(f'- {dts.name}', file=str_out)
            result = runner.run(tests)
            print_test_result(result)
            proceed &= proceed
        print('+'*70,file=str_out)
    # !SECTION - run unit tests
    # SECTION - run integration tests
    print('+'*70)
    print('+'*70,file=str_out)
    if not proceed:
        prompt = 'Skipping integration test suites.'
        print(prompt)
        print(f'{prompt}',file=str_out)
    else:
        prompt = 'Running integration test suites:'
        print(prompt)
        print(f'{prompt}',file=str_out)
        integ_tests_available = _suites_integ_test.keys()
        for dts in desired_test_suites:
            if dts not in integ_tests_available:
                continue
            tests = unittest.TestSuite()
            tests.addTests(_suites_integ_test[dts])
            print(f'    {dts.name}... ', end='')
            print(f'- {dts.name}', file=str_out)
            result = runner.run(tests)
            print_test_result(result)
        print('+'*70,file=str_out)
    # !SECTION - run integration tests
    # -----   -----
    # NOTE - show suites that was not found
    if len(not_found_test_suites) > 0:
        print(str_suites_not_found)
    # -----   -----
    with open(file=f'{file_directory}/test-{file_name}.txt',
              mode='w', encoding='utf-8') as fp:
        print(str_out.getvalue(), file=fp)
    # -----   -----


if __name__ == "__main__":
    main(sys.argv[1:])
