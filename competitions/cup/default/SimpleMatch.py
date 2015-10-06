# -*- coding: utf-8  -*-
"""Simple default match simulator."""

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

import random


class SimpleMatch(object):
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.score1 = ''
        self.score2 = ''

    def __str__(self):
        return '{0} {1} - {2} {3}'.format(self.team1, self.score1,
                                          self.score2, self.team2)

    def shortstr(self):
        return '{0}-{1}'.format(self.score1, self.score2)

    def play(self):
        score1 = 0
        score2 = 0
        for __ in range(25):
            num1 = random.randint(0, 100)
            num2 = random.randint(0, 100)
            if num1 > num2:
                score1 += 1
            elif num2 > num1:
                score2 += 1
        if score1 > score2:
            self.winner = self.team1
        elif score2 > score1:
            self.winner = self.team2
        else:
            self.winner = None
        self.score1 = score1
        self.score2 = score2
