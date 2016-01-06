# -*- coding: utf-8  -*-
"""Losers bracket for a double-elimination cup for powers of two."""

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

from competitions.cup import CupFinished
from competitions.match import config


class PowerOfTwoLosersBracket(object):

    """Double-elimination cup losers bracket for powers of two (4, 8, 16, etc.)."""

    def __init__(self, rounds=0):
        """Constructor.

        @param rounds: The number of rounds in the corresponding winners bracket
        @type rounds: int
        """
        Match = config.base_match

        self.index = [0, -1]
        self.round_count = (rounds - 1) // 2

        self.matches = []
        match_count = 2 ** (rounds - 2)
        self.matches.append([Match("Match {} Loser".format(2 * i + 1),
                                   "Match {} Loser".format(2 * i + 2))
                             for i in range(match_count)])
        winners_matches = self._generate_winner_nums(rounds)
        winners_match_index = 0
        losers_match_num = 1
        for __ in range(rounds - 1):
            round = []
            for ___ in range(match_count):
                round.append(Match('Match {} Loser'.format(winners_matches[winners_match_index]),
                                   'Match L{} Winner'.format(losers_match_num)))
                winners_match_index += 1
                losers_match_num += 1
            self.matches.append(round)
            if match_count == 1:
                break
            match_count //= 2
            round = []
            for ___ in range(match_count):
                round.append(Match('Match L{} Winner'.format(losers_match_num),
                                   'Match L{} Winner'.format(losers_match_num + 1)))
                losers_match_num += 2
            self.matches.append(round)

    def _generate_winner_nums(self, rounds):
        """Generate the list of winners bracket match numbers.

        @param rounds: The number of rounds
        @type rounds: int
        """
        match_index = 2 ** (rounds - 1)
        match_nums = []
        for i in range(match_index // 2):
            match_nums.append(match_index + 2)
            match_nums.append(match_index + 1)
            match_index += 2
        del match_nums[-2]
        return match_nums

    def play_match(self):
        """Play a cup match.

        @return: The winner of the simulated match
        @raise CupFinished: If the cup is finished
        """
        self.index[1] += 1
        round = self.matches[self.index[0]]
        is_minor = self.index[0] % 2 == 0
        match = None
        try:
            match = round[self.index[1]]
        except IndexError:
            self.index[0] += 1
            self.index[1] = 0
            round = self.matches[self.index[0]]
            is_minor = self.index[0] % 2 == 0
            match = round[0]
        winner = None
        while not winner:
            match.play()
            winner = match.winner
        try:
            if is_minor:
                next_match = self.matches[self.index[0] + 1][self.index[1]]
                next_match.team2 = winner
            else:
                next_match = self.matches[self.index[0] + 1][self.index[1] // 2]
                if self.index[1] % 2 == 0:
                    next_match.team1 = winner
                else:
                    next_match.team2 = winner
        except IndexError:
            self.winner = winner
            raise CupFinished(winner)

        return winner
