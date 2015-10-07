# -*- coding: utf-8  -*-
"""Single-elimination cup for powers of two."""

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

from competitions.cup import getCupMatchClass


Match = getCupMatchClass()


class PowerOfTwoSingleEliminationCup(object):
    def __init__(self, rounds=0, teams=[]):
        """Constructor."""
        self.index = [0, -1]
        self.round_count = rounds
        self.team_count = 2 ** rounds
        if not teams:
            self.teams = list(map(lambda x: 'Team ' + str(x),
                                  range(1, self.team_count + 1)))
        else:
            self.teams = teams
        self.matches = []
        match_count = self.team_count / 2
        self.matches.append([Match(self.teams[i * 2], self.teams[i * 2 + 1])
                             for i in range(match_count)])
        match_num = 1
        for __ in range(1, rounds):
            match_count /= 2
            round = []
            for ___ in range(match_count):
                round.append(Match('Match {} Winner'.format(match_num),
                                   'Match {} Winner'.format(match_num + 1)))
                match_num += 2
            self.matches.append(round)

    def play_match(self):
        """Play a cup match."""
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
        """Update first-round matches."""
        first_round = self.matches[0]
        for x in range(len(first_round)):
            first_round[x].team1 = self.teams[x * 2]
            first_round[x].team2 = self.teams[x * 2 + 1]

    def print_cup(self):
        """Print the cup to the console."""
        space = ' ' * 40
        line_count = self.team_count * 2 - 1
        lines = [[] for __ in range(line_count)]
        first_team = True
        for round in range(self.round_count):
            match_num = 0
            div = int(2 * 2 ** round)
            mod = int(div / 2 - 1)
            for i in range(line_count):
                if i % div == mod:
                    if first_team:
                        lines[i].append('{:<30}'.format(self.matches[round][match_num].team1) +
                                        ' ' +
                                        '{:>4}'.format(self.matches[round][match_num].score1) +
                                        ' ' * 5)
                    else:
                        lines[i].append('{:<30}'.format(self.matches[round][match_num].team2) +
                                        ' ' +
                                        '{:>4}'.format(self.matches[round][match_num].score2) +
                                        ' ' * 5)
                        match_num += 1
                    first_team = not first_team
                else:
                    lines[i].append(space)
        for line in lines:
            print ''.join(line)
