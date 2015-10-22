# -*- coding: utf-8  -*-
"""Tests for cup class registration and use."""

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

from . import TestCase

from competitions.cup import CupConfig, config
from competitions.cup.default.PowerOfTwoSingleEliminationCup import PowerOfTwoSingleEliminationCup


class TestCupRegistration(TestCase):

    """Tests for cup class finding."""

    def test_basic(self):
        """Test loading of cup classes."""
        self.assertEqual(config.cup('competitions.poweroftwo_single'),
                         PowerOfTwoSingleEliminationCup)
        self.assertRaises(KeyError, config.cup, 'competitions.unused')

    def test_singleton(self):
        """Test to ensure the configuration object's singleton status."""
        self.assertRaises(RuntimeError, CupConfig)
