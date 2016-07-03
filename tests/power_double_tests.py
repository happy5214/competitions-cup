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

from competitions.match import config as match_config
from competitions.cup import CupFinished, config as cup_config
from competitions.cup.default.PowerOfTwoDoubleEliminationCup import PowerOfTwoDoubleEliminationCup
from competitions.cup.default.PowerOfTwoLosersBracket import PowerOfTwoLosersBracket

if PY3:
    unicode = str


CupClass = cup_config.cup('competitions.poweroftwo_double')


class TestPowerOfTwoDoubleEliminationCup(TestCase):

    """Tests for standard double-elimination cup for powers of two."""

    @classmethod
    def setUpClass(cls):
        """Class setup code."""
        match_config.base_match = 'competitions.test'

    def test_class_loading(self):
        """Test the equality of class loaded through setuptools with direct import."""
        self.assertEqual(CupClass, PowerOfTwoDoubleEliminationCup,
                         'Classes not the same.')

    def test_default_team_list(self):
        """Test the automatically generated default team list."""
        cup = CupClass(rounds=2)
        list_of_teams = ['Team 1', 'Team 2', 'Team 3', 'Team 4']
        self.assertListEqual(cup.teams, list_of_teams)

    def test_team_count_validation(self):
        """Test team count checking in constructor."""
        teams = ['Team' for __ in range(7)]
        self.assertRaises(ValueError, CupClass,
                          rounds=2, teams=teams)
        teams = ['Team' for __ in range(4)]
        self.assertRaises(ValueError, CupClass,
                          rounds=3, teams=teams)
        teams = ['Team' for __ in range(16)]
        CupClass(rounds=4, teams=teams)

    def test_teams_used(self):
        """Test that provided teams are used."""
        teams = ['Team' for __ in range(8)]
        teams[5] = 'Special'
        cup = CupClass(rounds=3, teams=teams)
        self.assertEqual(teams[0], cup.winners_bracket.matches[0][0].team1,
                         'First team not used.')
        self.assertEqual(cup.winners_bracket.matches[0][2].team2, 'Special',
                         'Special team not used.')

    def test_teams_redone(self):
        """Test that update_teams resets first round."""
        teams = ['Team' for __ in range(8)]
        teams[5] = 'Special'
        cup = CupClass(rounds=3, teams=teams)
        self.assertEqual(teams[0], cup.winners_bracket.matches[0][0].team1,
                         'First team not used.')
        self.assertEqual(cup.winners_bracket.matches[0][2].team2, 'Special',
                         'Special team not used.')
        new_teams = ['New' for __ in range(8)]
        new_teams[2] = 'New Special'
        cup.update_teams(new_teams)
        self.assertEqual(new_teams[0], cup.winners_bracket.matches[0][0].team1,
                         'First team not updated.')
        self.assertEqual(cup.winners_bracket.matches[0][1].team1, 'New Special',
                         'New special team not updated.')
        self.assertNotEqual(cup.winners_bracket.matches[0][2].team2, 'Special',
                            'Old special team not updated.')

    def test_cup_results(self):
        """Test the results of playing cup."""
        teams = ['Team {}'.format(x + 1) for x in range(8)]
        cup = CupClass(rounds=3, teams=teams)
        for i in range(13):
            self.assertIsInstance(cup.play_match(), unicode, 'Cup ended early.')
        self.assertRaises(CupFinished, cup.play_match)
        final_match = cup.final
        self.assertEqual(final_match.team1, teams[0], 'First finalist is wrong.')
        self.assertEqual(final_match.team2, teams[4], 'Second finalist is wrong.')
        self.assertEqual(cup.winner, 'Team 1', 'Cup has wrong winner.')

    def test_replay(self):
        """Test replaying the final depending on the winner."""
        teams = ['Team {}'.format(x + 1) for x in range(8)]
        cup = CupClass(rounds=3, teams=teams)
        for i in range(13):
            self.assertIsInstance(cup.play_match(), unicode, 'Cup ended early.')
        cup.final.team1, cup.final.team2 = cup.final.team2, cup.final.team1
        self.assertRaises(CupFinished, cup.play_match)
        final_match = cup.final
        self.assertEqual(final_match.team1, teams[4], 'Flipped first finalist is wrong.')
        self.assertEqual(final_match.team2, teams[0], 'Flipped second finalist is wrong.')
        self.assertEqual(cup.winner, 'Team 5', 'Cup has wrong winner.')

    def test_cup_printout(self):
        """Test the printout of the cup when completed."""
        teams = ['Team {}'.format(x + 1) for x in range(8)]
        cup = CupClass(rounds=3, teams=teams)
        cup.play_cup()
        expected_string = (
            '\n'
            'Team 1                            5     '
            '                                        '
            '                                        '
            '\n'
            '                                        '
            'Team 1                            5     '
            '                                        '
            '\n'
            'Team 2                            0     '
            '                                        '
            '                                        '
            '\n'
            '                                        '
            '                                        '
            'Team 1                            5     '
            '\n'
            'Team 3                            5     '
            '                                        '
            '                                        '
            '\n'
            '                                        '
            'Team 3                            0     '
            '                                        '
            '\n'
            'Team 4                            0     '
            '                                        '
            '                                        '
            '\n'
            '                                        '
            '                                        '
            '                                        '
            '\n'
            'Team 5                            5     '
            '                                        '
            '                                        '
            '\n'
            '                                        '
            'Team 5                            5     '
            '                                        '
            '\n'
            'Team 6                            0     '
            '                                        '
            '                                        '
            '\n'
            '                                        '
            '                                        '
            'Team 5                            0     '
            '\n'
            'Team 7                            5     '
            '                                        '
            '                                        '
            '\n'
            '                                        '
            'Team 7                            0     '
            '                                        '
            '\n'
            'Team 8                            0     '
            '                                        '
            '                                        '
            '\n\n'
            '                                        '
            '                                        '
            '                                        '
            'Team 5                            5     '
            '\n'
            '                                        '
            'Team 7                            5     '
            '                                        '
            '                                        '
            '\n'
            'Team 2                            5     '
            '                                        '
            'Team 7                            5     '
            '                                        '
            '\n'
            '                                        '
            'Team 2                            0     '
            '                                        '
            '                                        '
            '\n'
            'Team 4                            0     '
            '                                        '
            '                                        '
            'Team 7                            0     '
            '\n'
            '                                        '
            'Team 3                            5     '
            '                                        '
            '                                        '
            '\n'
            'Team 6                            5     '
            '                                        '
            'Team 3                            0     '
            '                                        '
            '\n'
            '                                        '
            'Team 6                            0     '
            '                                        '
            '                                        '
            '\n'
            'Team 8                            0     '
            '                                        '
            '                                        '
            '                                        '
            '\n\n\n'
            'Team 1                            5          '
            '                                             '
            '\n'
            '                                             '
            '                                             '
            '\n'
            'Team 5                            0          '
            '                                             '
            '\n'
        )
        self.assertEqual(cup.print_cup(), expected_string,
                         'Wrong bracket printed.')


class TestPowerOfTwoLosersBracket(TestCase):

    """Tests for losers bracket of standard double-elimination cup for powers of two."""

    @classmethod
    def setUpClass(cls):
        """Class setup code."""
        match_config.base_match = 'competitions.test'

    def test_round_count(self):
        """Test the bracket's round count."""
        self.assertRaises(ValueError, PowerOfTwoLosersBracket, rounds=1)
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
            '\n'
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
            '\n'
        )
        self.assertEqual(bracket.print_cup(), expected_string,
                         'Wrong bracket printed.')
