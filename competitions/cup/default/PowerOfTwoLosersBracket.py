# -*- coding: utf-8  -*-
"""Losers bracket for a double-elimination cup for powers of two."""

# Copyright (C) 2016 Alexander Jones
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

from competitions.cup import StandardBracket, CupFinished, init_nested_list
from competitions.match import config


class PowerOfTwoLosersBracket(StandardBracket):

    """Double-elimination cup losers bracket for powers of two (4, 8, 16, etc.)."""

    def __init__(self, rounds=0):
        """Constructor.

        @param rounds: The number of rounds in the corresponding winners bracket
        @type rounds: int
        """
        super(PowerOfTwoLosersBracket, self).__init__()  # Parent constructor

        # Parameter validation
        if rounds < 2:
            raise ValueError('Not enough rounds.')

        Match = config.base_match  # Load match class

        # Object constants
        self.winners_round_count = rounds
        self.phases = rounds - 1
        self.round_count = self.phases * 2

        # Build bracket
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
        self._generate_loser_placements()

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

    def _generate_loser_placements(self):
        """Generate the placements for winners bracket losers."""
        placements = []
        for phase in range(self.phases):
            pairs = 2 ** max(self.phases - phase - 2, 0)
            for pair in range(pairs):
                placements.append(((phase * 2 + 1), (pair * 2 + 1)))
                placements.append(((phase * 2 + 1), (pair * 2)))
        del placements[-2]
        self._loser_placements = placements
        self._current_loser_placement = self._first_round_loser_placement = 0
        self._first_round_teams = len(placements) + 1

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
            is_minor = self.index[0] % 2 == 0
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

    def add_team(self, team):
        """Add a loser from the winners bracket to the losers bracket.

        @param team: The team to add
        @type team: A str or team-like object
        """
        if self._first_round_loser_placement < self._first_round_teams:
            index = self._first_round_loser_placement
            match = self.matches[0][index // 2]
            if index % 2 == 0:
                match.team1 = team
            else:
                match.team2 = team
            self._first_round_loser_placement += 1
        else:
            position = self._loser_placements[self._current_loser_placement]
            match = self.matches[position[0]][position[1]]
            match.team1 = team
            self._current_loser_placement += 1

    def print_cup(self, display=True):
        """Print the cup to a string and (optionally) the console.

        @param display: Whether to print to the console.
        @type display: bool
        @return: The displayed bracket
        @rtype: str
        """
        space = ' ' * 40
        first = 2 ** (self.phases - 1)
        line_count = first * 5 - 1
        lines = init_nested_list(line_count)
        first_team = True
        team_str = self._bracket_match_str
        for phase in range(self.phases):
            first = 2 ** (self.phases - 1)
            match_num = 0
            round = phase * 2
            div = 2 * 2 ** phase
            for i in range(first):
                lines[i].append(space)
            for i in range(first, line_count):
                (match_num, first_team) = team_str(((i - first) % div == 0),
                                                   lines[i], round, match_num,
                                                   first_team)
            # Major round
            match_num = 0
            first -= 2 ** phase
            round += 1
            for i in range(first):
                lines[i].append(space)
            for i in range(first, line_count):
                try:
                    (match_num, first_team) = team_str(((i - first) % div == 0),
                                                       lines[i], round,
                                                       match_num, first_team)
                except IndexError:
                    lines[i].append(space)
        return self._actually_print_bracket(lines, display)
