# -*- coding: utf-8  -*-
"""Tests for standard single-elimination cups."""

# Copyright (C) 2015, 2016, 2017 Alexander Jones
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
from competitions.cup.default.single_elimination import StandardSingleEliminationCup
from competitions.match.default.TestMatch import TestMatch

if PY3:
    unicode = str


CupClass = StandardSingleEliminationCup
MatchClass = TestMatch


class TestStandardSingleEliminationCup(TestCase):

    """Tests for standard single-elimination cups."""

    def test_default_team_list(self):
        """Test the automatically generated default team list."""
        cup = CupClass(match_class=MatchClass, rounds=2)
        list_of_teams = ['Team 1', 'Team 2', 'Team 3', 'Team 4']
        self.assertListEqual(cup.teams, list_of_teams)

    def test_team_count_validation(self):
        """Test team count checking in constructor."""
        teams = ['Team' for __ in range(7)]
        self.assertRaises(ValueError, CupClass,
                          match_class=MatchClass,
                          rounds=2, teams=teams)
        teams = ['Team' for __ in range(4)]
        self.assertRaises(ValueError, CupClass,
                          match_class=MatchClass,
                          rounds=3, teams=teams)
        teams = ['Team' for __ in range(16)]
        CupClass(match_class=MatchClass, rounds=4, teams=teams)

    def test_teams_used(self):
        """Test that provided teams are used."""
        teams = ['Team' for __ in range(8)]
        teams[5] = 'Special'
        cup = CupClass(match_class=MatchClass, rounds=3, teams=teams)
        self.assertEqual(teams[0], cup.matches[0][0].team1, 'First team not used.')
        self.assertEqual(cup.matches[0][2].team2, 'Special', 'Special team not used.')

    def test_teams_redone(self):
        """Test that update_teams resets first round."""
        teams = ['Team' for __ in range(8)]
        teams[5] = 'Special'
        cup = CupClass(match_class=MatchClass, rounds=3, teams=teams)
        self.assertEqual(teams[0], cup.matches[0][0].team1, 'First team not used.')
        self.assertEqual(cup.matches[0][2].team2, 'Special', 'Special team not used.')
        new_teams = ['New' for __ in range(8)]
        new_teams[2] = 'New Special'
        cup.update_teams(new_teams)
        self.assertEqual(new_teams[0], cup.matches[0][0].team1, 'First team not updated.')
        self.assertEqual(cup.matches[0][1].team1, 'New Special', 'New special team not updated.')
        self.assertNotEqual(cup.matches[0][2].team2, 'Special', 'Old special team not updated.')

    def test_cup_results(self):
        """Test the results of playing cup."""
        teams = ['Team {}'.format(x + 1) for x in range(8)]
        teams[3] = None
        cup = CupClass(match_class=MatchClass, rounds=3, teams=teams)
        for __ in range(5):
            self.assertIsInstance(cup.play_match(), unicode, 'Cup ended early.')
        self.assertRaises(CupFinished, cup.play_match)
        sf1_match = cup.matches[1][0]
        self.assertEqual(sf1_match.team2, teams[2], 'Walkover not awarded.')
        final_match = cup.matches[2][0]
        self.assertEqual(final_match.team1, teams[0], 'First finalist is wrong.')
        self.assertEqual(final_match.team2, teams[4], 'Second finalist is wrong.')
        self.assertEqual(cup.winner, 'Team 1', 'Cup has wrong winner.')

    def test_cup_printout(self):
        """Test the printout of the cup when completed."""
        teams = ['Team {}'.format(x + 1) for x in range(8)]
        teams[2] = None
        cup = CupClass(match_class=MatchClass, rounds=3, teams=teams)
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
            '                                        '
            '                                        '
            '                                        '
            '\n'
            '                                        '
            'Team 4                            0     '
            '                                        '
            '\n'
            '                                        '
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
            '\n'
        )
        self.assertEqual(cup.print_cup(), expected_string,
                         'Wrong bracket printed.')
