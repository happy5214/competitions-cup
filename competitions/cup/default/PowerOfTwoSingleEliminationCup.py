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
from competitions.cup import StandardCup, CupFinished, init_nested_list


class PowerOfTwoSingleEliminationCup(StandardCup):

    """Standard single-elimination cup for powers of two (4, 8, 16, etc.)."""

    def __init__(self, rounds=0, teams=[]):
        """Constructor.

        @param rounds: The number of rounds
        @type rounds: int
        @param teams: An optional list of teams
        @type teams: list
        """
        super(PowerOfTwoSingleEliminationCup, self).__init__(teams=teams,
                                                             team_count=2 ** rounds)
        Match = config.base_match

        self.round_count = rounds

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

    def play_match(self):
        """Play a cup match.

        @return: The winner of the simulated match
        @raise CupFinished: If the cup is finished
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
        self.current_match = match
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
            raise CupFinished(winner)

        return winner

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
        line_count = self.team_count * 2 - 1
        lines = init_nested_list(line_count)
        first_team = True
        team_str = self._bracket_match_str
        for round in range(self.round_count):
            match_num = 0
            div = 2 * 2 ** round
            mod = div // 2 - 1
            for i in range(line_count):
                (match_num, first_team) = team_str((i % div == mod), lines[i],
                                                   round, match_num,
                                                   first_team)
        return self._actually_print_bracket(lines, display)
