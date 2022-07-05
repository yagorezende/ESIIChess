import unittest
from typing import Dict, List

import tests.test_suites as ts
import logic.referee


class TestReferee(unittest.TestCase):
    def setUp(self) -> None:
        self.referee = logic.referee.Referee([],{},'w')
        return None

    def tearDown(self) -> None:
        self.referee = None
        return None

    def test_(self) -> None:
        return None


def suites() -> Dict[ts.TestSuites, List[unittest.TestCase]]:
    return {
        ts.TestSuites.GAME_LOGIC: [
            TestReferee(''),
            TestReferee('')],
        ts.TestSuites.GAME_TIES: [
            TestReferee('')],
        ts.TestSuites.SMOKE_TESTING: [
            TestReferee('')]
    }
