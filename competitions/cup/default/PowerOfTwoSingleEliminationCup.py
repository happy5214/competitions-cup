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

from __future__ import print_function, unicode_literals

from competitions.match import config


class PowerOfTwoSingleEliminationCup(object):

    """Standard single-elimination cup for powers of two (4, 8, 16, etc.)."""

    def __init__(self, rounds=0, teams=[]):
        """Constructor.

        @param rounds: The number of rounds
        @type rounds: int
        @param teams: An optional list of teams
        @type teams: list
        """
        Match = config.base_match

        self.index = [0, -1]
        self.winner = None
        self.round_count = rounds
        self.team_count = 2 ** rounds
        if not teams:
            self.teams = list(map(lambda x: 'Team ' + str(x),
                                  range(1, self.team_count + 1)))
        else:
            if len(teams) != self.team_count:
                raise ValueError('Wrong number of teams')
            self.teams = teams
        self.matches = []
        match_count = self.team_count // 2
        self.matches.append([Match(self.teams[i * 2], self.teams[i * 2 + 1])
                             for i in range(match_count)])
        match_num = 1
        for __ in range(1, rounds):
            match_count //= 2
            round = []
            for ___ in range(match_count):
                round.append(Match('Match {} Winner'.format(match_num),
                                   'Match {} Winner'.format(match_num + 1)))
                match_num += 2
            self.matches.append(round)

    def play_cup(self):
        """Play the whole cup."""
        while not self.play_match():
            pass
        return self.winner

    def play_match(self):
        """Play a cup match.

        @return: Whether the cup has concluded
        @rtype: bool
        """
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
            next_match = self.matches[self.index[0] + 1][self.index[1] // 2]
            if self.index[1] % 2 == 0:
                next_match.team1 = winner
            else:
                next_match.team2 = winner
        except IndexError:
            self.winner = winner
            return True

        return False

    def update_teams(self, teams):
        """Update the list of teams and the first-round matches.

        @param teams: The new list of teams
        @type teams: list
        """
        self.teams = teams
        first_round = self.matches[0]
        for x in range(len(first_round)):
            first_round[x].team1 = self.teams[x * 2]
            first_round[x].team2 = self.teams[x * 2 + 1]

    def print_cup(self, display=True):
        """Print the cup to a string and (optionally) the console.

        @param display: Whether to print to the console.
        @type display: bool
        @return: The displayed bracket
        @rtype: str
        """
        space = ' ' * 40
        line_count = self.team_count * 2 - 1
        lines = [[] for __ in range(line_count)]
        first_team = True
        for round in range(self.round_count):
            match_num = 0
            div = 2 * 2 ** round
            mod = div // 2 - 1
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
        bracket = '\n'.join([''.join(line) for line in lines])
        if display:
            print(bracket)
        return bracket
