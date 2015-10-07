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

from . import TestCase, TestMatch

import competitions.cup
from competitions.cup.default.PowerOfTwoSingleEliminationCup import PowerOfTwoSingleEliminationCup


class TestPowerOfTwoSingleEliminationCup(TestCase):

    """Tests for standard single-elimination cup for powers of two."""

    @classmethod
    def setUpClass(cls):
        competitions.cup.setCupMatchClass(TestMatch)

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
