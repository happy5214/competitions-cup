# -*- coding: utf-8  -*-
"""Tests for standard single-elimination cups for powers of two."""

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

from . import TestCase

from competitions.match import config
from competitions.cup.default.PowerOfTwoSingleEliminationCup import PowerOfTwoSingleEliminationCup


class TestPowerOfTwoSingleEliminationCup(TestCase):

    """Tests for standard single-elimination cup for powers of two."""

    @classmethod
    def setUpClass(cls):
        """Class setup code."""
        config.base_match = 'competitions.test'

    def test_default_team_list(self):
        """Test the automatically generated default team list."""
        cup = PowerOfTwoSingleEliminationCup(rounds=2)
        list_of_teams = ['Team 1', 'Team 2', 'Team 3', 'Team 4']
        self.assertListEqual(cup.teams, list_of_teams)

    def test_team_count_validation(self):
        """Test team count checking in constructor."""
        teams = ['Team' for __ in range(7)]
        self.assertRaises(ValueError, PowerOfTwoSingleEliminationCup,
                          rounds=2, teams=teams)
        teams = ['Team' for __ in range(4)]
        self.assertRaises(ValueError, PowerOfTwoSingleEliminationCup,
                          rounds=3, teams=teams)
        teams = ['Team' for __ in range(16)]
        PowerOfTwoSingleEliminationCup(rounds=4, teams=teams)

    def test_teams_used(self):
        """Test that provided teams are used."""
        teams = ['Team' for __ in range(8)]
        teams[5] = 'Special'
        cup = PowerOfTwoSingleEliminationCup(rounds=3, teams=teams)
        self.assertEqual(teams[0], cup.matches[0][0].team1, 'First team not used.')
        self.assertEqual(cup.matches[0][2].team2, 'Special', 'Special team not used.')

    def test_teams_redone(self):
        """Test that update_teams resets first round."""
        teams = ['Team' for __ in range(8)]
        teams[5] = 'Special'
        cup = PowerOfTwoSingleEliminationCup(rounds=3, teams=teams)
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
        cup = PowerOfTwoSingleEliminationCup(rounds=3, teams=teams)
        for i in range(6):
            self.assertFalse(cup.play_match(), 'Cup ended early.')
        self.assertTrue(cup.play_match(), 'Cup still has not ended.')
        final_match = cup.matches[2][0]
        self.assertEqual(final_match.team1, teams[0], 'First finalist is wrong.')
        self.assertEqual(final_match.team2, teams[4], 'Second finalist is wrong.')
        self.assertEqual(cup.winner, 'Team 1', 'Cup has wrong winner.')
