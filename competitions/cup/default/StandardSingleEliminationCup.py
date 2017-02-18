# -*- coding: utf-8  -*-
"""Standard single-elimination cup."""

# Copyright (C) 2015-16 Alexander Jones
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

from competitions.cup import StandardCup, init_nested_list


class StandardSingleEliminationCup(StandardCup):

    """Standard single-elimination cup."""

    def __init__(self, match_class, rounds=0, teams=[]):
        """Constructor.

        @param rounds: The number of rounds
        @type rounds: int
        @param teams: An optional list of teams
        @type teams: list
        """
        super(StandardSingleEliminationCup, self).__init__(match_class=match_class,
                                                           teams=teams,
                                                           team_count=2 ** rounds,
                                                           rounds=rounds)

    def _build_second_round(self, match_count, match_num):
        """Build the bracket's second round."""
        Match = self.MatchClass
        round = []
        for ___ in range(match_count):
            teams = []
            for i in range(2):
                previous_match = self.matches[0][match_num + i - 1]
                if not previous_match.is_walkover:
                    teams.append('Match {} Winner'.format(match_num + i))
                else:
                    teams.append(previous_match.team1 or previous_match.team2)
            round.append(Match(teams[0], teams[1]))
            match_num += 2
        self.matches.append(round)
        return match_num

    def _build_bracket(self):
        """Build the nested list representing the bracket."""
        Match = self.MatchClass
        match_count = self.team_count // 2
        self.matches.append([Match(self.teams[i * 2], self.teams[i * 2 + 1])
                             for i in range(match_count)])
        match_num = 1
        match_count //= 2
        match_num = self._build_second_round(match_count, match_num)
        for __ in range(2, self.round_count):
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

    def _set_current_match(self):
        """Set the current match."""
        super(StandardSingleEliminationCup, self)._set_current_match()
        while self.current_match.is_walkover:
            super(StandardSingleEliminationCup, self)._set_current_match()

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
