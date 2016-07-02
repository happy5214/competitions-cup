# -*- coding: utf-8  -*-
"""Stepladder cup."""

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
from competitions.cup import StandardCup


class StepladderCup(StandardCup):

    """Standard stepladder cup for any number of teams."""

    def __init__(self, teams):
        """Constructor.

        @param teams: A list or number of teams
        @type teams: list or int
        """
        if isinstance(teams, int):
            super(StepladderCup, self).__init__(teams=[],
                                                team_count=teams)
        else:
            super(StepladderCup, self).__init__(teams=teams,
                                                team_count=len(teams))
        Match = config.base_match

        self.round_count = self.team_count - 1

        self.matches.append([Match(self.teams[0], self.teams[1])])
        for x in range(2, self.team_count):
            self.matches.append([Match(self.teams[x], 'Match {} Winner'.format(x - 1))])

    def _assign_winner(self, winner):
        """Assign winner to their next match."""
        next_match = self.matches[self.index[0] + 1][0]
        next_match.team2 = winner

    def update_teams(self, teams):
        """Update the list of teams and the seedings.

        @param teams: The new list of teams
        @type teams: list
        """
        self.teams = teams
        self.matches[0][0].team1 = teams[0]
        self.matches[0][0].team2 = teams[1]
        for x in range(2, self.team_count):
            self.matches[x - 1][0].team1 = teams[x]

    def _print_bracket_lines(self):
        """Generate the bracket lines to be printed."""
        space = ' ' * 40
        line_count = self.team_count + 1
        lines = [[] for __ in range(line_count)]
        for round in range(self.round_count):
            line_num = self.round_count - round - 1
            for x in range(line_num):
                lines[x].append(space)
            lines[line_num].append('{:<30}'.format(self.matches[round][0].team1) +
                                   ' ' +
                                   '{:>4}'.format(self.matches[round][0].score1) +
                                   ' ' * 5)
            line_num += 1
            lines[line_num].append(space)
            line_num += 1
            lines[line_num].append('{:<30}'.format(self.matches[round][0].team2) +
                                   ' ' +
                                   '{:>4}'.format(self.matches[round][0].score2) +
                                   ' ' * 5)
            for x in range(line_num + 1, line_count):
                lines[x].append(space)
        return lines
