# -*- coding: utf-8  -*-
"""Tests for standard stepladder cups."""

# Copyright (C) 2015 Alexander Jones
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
from competitions.cup.default.StepladderCup import StepladderCup

if PY3:
    unicode = str


CupClass = cup_config.cup('competitions.stepladder')


class TestStepladderCup(TestCase):

    """Tests for standard stepladder cups."""

    @classmethod
    def setUpClass(cls):
        """Class setup code."""
        match_config.base_match = 'competitions.test'

    def test_class_loading(self):
        """Test the equality of class loaded through setuptools with direct import."""
        self.assertEqual(CupClass, StepladderCup, 'Classes not the same.')

    def test_default_team_list(self):
        """Test the automatically generated default team list."""
        cup = CupClass(teams=4)
        list_of_teams = ['Team 1', 'Team 2', 'Team 3', 'Team 4']
        self.assertListEqual(cup.teams, list_of_teams)

    def test_teams_used(self):
        """Test that provided teams are used."""
        teams = ['Team' for __ in range(8)]
        teams[5] = 'Special'
        cup = CupClass(teams=teams)
        self.assertEqual(teams[0], cup.matches[0].team1, 'First team not used.')
        self.assertEqual(cup.matches[4].team1, 'Special', 'Special team not used.')

    def test_teams_redone(self):
        """Test that update_teams resets first round."""
        teams = ['Team' for __ in range(8)]
        teams[5] = 'Special'
        cup = CupClass(teams=teams)
        self.assertEqual(teams[0], cup.matches[0].team1, 'First team not used.')
        self.assertEqual(cup.matches[4].team1, 'Special', 'Special team not used.')
        new_teams = ['New' for __ in range(8)]
        new_teams[2] = 'New Special'
        cup.update_teams(new_teams)
        self.assertEqual(new_teams[0], cup.matches[0].team1, 'First team not updated.')
        self.assertEqual(cup.matches[1].team1, 'New Special', 'New special team not updated.')
        self.assertNotEqual(cup.matches[4].team1, 'Special', 'Old special team not updated.')

    def test_cup_results(self):
        """Test the results of playing cup."""
        teams = ['Team {}'.format(x + 1) for x in range(8)]
        cup = CupClass(teams=teams)
        for i in range(6):
            self.assertIsInstance(cup.play_match(), unicode, 'Cup ended early.')
        self.assertRaises(CupFinished, cup.play_match)
        final_match = cup.matches[6]
        self.assertEqual(final_match.team1, teams[7], 'First finalist is wrong.')
        self.assertEqual(final_match.team2, teams[6], 'Second finalist is wrong.')
        self.assertEqual(cup.winner, 'Team 8', 'Cup has wrong winner.')

    def test_cup_printout(self):
        """Test the printout of the cup when completed."""
        teams = ['Team {}'.format(x + 1) for x in range(8)]
        cup = CupClass(teams=teams)
        cup.play_cup()
        expected_string = (
            '                                        '
            '                                        '
            '                                        '
            '                                        '
            '                                        '
            '                                        '
            'Team 8                            5     '
            '\n'
            '                                        '
            '                                        '
            '                                        '
            '                                        '
            '                                        '
            'Team 7                            5     '
            '                                        '
            '\n'
            '                                        '
            '                                        '
            '                                        '
            '                                        '
            'Team 6                            5     '
            '                                        '
            'Team 7                            0     '
            '\n'
            '                                        '
            '                                        '
            '                                        '
            'Team 5                            5     '
            '                                        '
            'Team 6                            0     '
            '                                        '
            '\n'
            '                                        '
            '                                        '
            'Team 4                            5     '
            '                                        '
            'Team 5                            0     '
            '                                        '
            '                                        '
            '\n'
            '                                        '
            'Team 3                            5     '
            '                                        '
            'Team 4                            0     '
            '                                        '
            '                                        '
            '                                        '
            '\n'
            'Team 1                            5     '
            '                                        '
            'Team 3                            0     '
            '                                        '
            '                                        '
            '                                        '
            '                                        '
            '\n'
            '                                        '
            'Team 1                            0     '
            '                                        '
            '                                        '
            '                                        '
            '                                        '
            '                                        '
            '\n'
            'Team 2                            0     '
            '                                        '
            '                                        '
            '                                        '
            '                                        '
            '                                        '
            '                                        '
        )
        self.assertEqual(cup.print_cup(), expected_string,
                         'Wrong bracket printed.')
