# -*- coding: utf-8  -*-
"""Tests for standard double-elimination cups for powers of two."""

# Copyright (C) 2016 Alexander Jones
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

# import unittest

from . import TestCase, PY3
from competitions.cup import CupFinished

from competitions.match import config as match_config
# from competitions.cup import CupFinished, config as cup_config
from competitions.cup.default.PowerOfTwoLosersBracket import PowerOfTwoLosersBracket

if PY3:
    unicode = str


# CupClass = cup_config.cup('competitions.poweroftwo_double')


class TestPowerOfTwoLosersBracket(TestCase):

    """Tests for losers bracket of standard double-elimination cup for powers of two."""

    @classmethod
    def setUpClass(cls):
        """Class setup code."""
        match_config.base_match = 'competitions.test'

    def test_round_count(self):
        """Test the bracket's round count."""
        for rounds in range(2, 6):
            bracket = PowerOfTwoLosersBracket(rounds=rounds)
            self.assertEqual(len(bracket.matches), ((rounds - 1) * 2),
                             "{}-team bracket has wrong number of rounds.".format(2 ** rounds))

    def test_bracket_results(self):
        """Test the results of playing losers bracket."""
        teams = ['Team {}'.format(x + 1) for x in range(7)]
        bracket = PowerOfTwoLosersBracket(rounds=3)
        for team in teams:
            bracket.add_team(team)
        for i in range(5):
            self.assertIsInstance(bracket.play_match(), unicode, 'Cup ended early.')
        self.assertRaises(CupFinished, bracket.play_match)
        final_match = bracket.matches[3][0]
        self.assertEqual(final_match.team1, teams[6], 'First finalist is wrong.')
        self.assertEqual(final_match.team2, teams[5], 'Second finalist is wrong.')
        self.assertEqual(bracket.winner, 'Team 7', 'Cup has wrong winner.')

    def test_bracket_printout(self):
        """Test the printout of the losers bracket when completed."""
        teams = ['Team {}'.format(x + 1) for x in range(7)]
        bracket = PowerOfTwoLosersBracket(rounds=3)
        for team in teams:
            bracket.add_team(team)
        try:
            while True:
                bracket.play_match()
        except CupFinished:
            pass
        expected_string = (
            '                                        '
            '                                        '
            '                                        '
            'Team 7                            5     '
            '\n'
            '                                        '
            'Team 6                            5     '
            '                                        '
            '                                        '
            '\n'
            'Team 1                            5     '
            '                                        '
            'Team 6                            5     '
            '                                        '
            '\n'
            '                                        '
            'Team 1                            0     '
            '                                        '
            '                                        '
            '\n'
            'Team 2                            0     '
            '                                        '
            '                                        '
            'Team 6                            0     '
            '\n'
            '                                        '
            'Team 5                            5     '
            '                                        '
            '                                        '
            '\n'
            'Team 3                            5     '
            '                                        '
            'Team 5                            0     '
            '                                        '
            '\n'
            '                                        '
            'Team 3                            0     '
            '                                        '
            '                                        '
            '\n'
            'Team 4                            0     '
            '                                        '
            '                                        '
            '                                        '
        )
        self.assertEqual(bracket.print_cup(display=False), expected_string,
                         'Wrong bracket printed.')
