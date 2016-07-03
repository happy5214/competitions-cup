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
from competitions.cup import StandardCup, init_nested_list


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

    def _assign_winner(self, winner):
        """Assign winner to their next match."""
        next_match = self.matches[self.index[0] + 1][self.index[1] // 2]
        if self.index[1] % 2 == 0:
            next_match.team1 = winner
        else:
            next_match.team2 = winner

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

    def _generate_layout(self):
        """Generate the bracket layout for display."""
        line_count = self.team_count * 2 - 1
        layout = init_nested_list(line_count)
        first_team = True
        match_gen = self._match_for_layout
        for round in range(self.round_count):
            match_num = 0
            div = 2 * 2 ** round
            mod = div // 2 - 1
            for i in range(line_count):
                (conf, layout_entry) = match_gen((i % div == mod),
                                                 round, match_num,
                                                 first_team)
                layout[i].append(layout_entry)
                (match_num, first_team) = conf
        return layout
