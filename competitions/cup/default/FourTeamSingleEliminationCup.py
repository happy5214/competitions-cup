# -*- coding: utf-8  -*-
"""Four-team single-elimination cup."""

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

from competitions.match import config


Match = config.base_match


class FourTeamSingleEliminationCup(object):
    def __init__(self, teams=[]):
        self.index = [0, -1]
        self.matches = [[Match('Team 1', 'Team 2'), Match('Team 3', 'Team 4')],
                        [Match('Match 1 Winner', 'Match 2 Winner')]]
        if not teams:
            self.teams = list(map(lambda x: 'Team ' + str(x), range(1, 5)))
        else:
            self.teams = teams

    def play_match(self):
        self.index[1] += 1
        round = self.matches[self.index[0]]
        match = None
        try:
            match = round[self.index[1]]
        except IndexError:
            self.index[0] += 1
            self.index[1] = 0
            round = self.matches[self.index[0]]
            match = round[0]
        winner = None
        while not winner:
            match.play()
            winner = match.winner
        try:
            next_match = self.matches[self.index[0] + 1][self.index[1] / 2]
            if self.index[1] % 2 == 0:
                next_match.team1 = winner
            else:
                next_match.team2 = winner
        except IndexError:
            return True

        return False

    def fix_first_round(self):
        first_round = self.matches[0]
        for x in range(len(first_round)):
            first_round[x].team1 = self.teams[x * 2]
            first_round[x].team2 = self.teams[x * 2 + 1]

    def print_cup(self):
        space = ' ' * 40
        lines = ['' for __ in range(7)]
        lines[0] = ('{:<30}'.format(self.matches[0][0].team1) + ' ' +
                    '{:>4}'.format(self.matches[0][0].score1) + ' ' * 5 +
                    space)
        lines[2] = ('{:<30}'.format(self.matches[0][0].team2) + ' ' +
                    '{:>4}'.format(self.matches[0][0].score2) + ' ' * 5 +
                    space)
        lines[4] = ('{:<30}'.format(self.matches[0][1].team1) + ' ' +
                    '{:>4}'.format(self.matches[0][1].score1) + ' ' * 5 +
                    space)
        lines[6] = ('{:<30}'.format(self.matches[0][1].team2) + ' ' +
                    '{:>4}'.format(self.matches[0][1].score2) + ' ' * 5 +
                    space)
        lines[1] = (space + '{:<30}'.format(self.matches[1][0].team1) + ' ' +
                    '{:>4}'.format(self.matches[1][0].score1) + ' ' * 5)
        lines[5] = (space + '{:<30}'.format(self.matches[1][0].team2) + ' ' +
                    '{:>4}'.format(self.matches[1][0].score2) + ' ' * 5)
        lines[3] = space * 2
        for line in lines:
            print line
