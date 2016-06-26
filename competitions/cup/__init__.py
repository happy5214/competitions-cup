# -*- coding: utf-8  -*-
"""Cup package."""

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

import pkg_resources


def init_nested_list(count):
    """Initialize an empty nested list.

    @param count: The length of the list
    @type count: int
    @return: A nested list
    @rtype: list
    """
    return [[] for __ in range(count)]


class Bracket(object):

    """Base class for tournament brackets."""

    def __init__(self):
        """Constructor."""
        self.winner = None
        self.matches = []
        self.index = [0, -1]

    def play_match(self):
        """Play a cup match.

        @return: The winner of the simulated match
        @raise CupFinished: If the cup is finished
        """
        raise NotImplementedError

    @property
    def round_over(self):
        """Whether the current round is over.

        @return: Whether the current round is over
        @rtype: bool
        """
        return (self.index[1] + 1) >= len(self.matches[self.index[0]])


class PrintableBracket(Bracket):

    """Mixin for a bracket printable to the console."""

    def _bracket_match_str(self, test, line, round_num, match_num, first_team):
        """Generate the string for a match to place in a printed bracket.

        @param test: Whether to print a team or a blank space
        @type test: bool
        @param line: The line to append the string to
        @type line: list
        @param round_num: The round number in self.matches
        @type round_num: int
        @param match_num: The match number for the round in self.matches
        @type match_num: int
        @param first_team: Whether to return the string for the first team
        @type first_team: bool
        @return: (match_num, False) if first_team and test are True,
                 (match_num + 1, True) if only test is True,
                 (match_num, first_team) otherwise
        @rtype: tuple
        """
        if test:
            match = self.matches[round_num][match_num]
            if first_team:
                team, score = match.team1, match.score1
            else:
                team, score = match.team2, match.score2
            line.append('{:<30} {:>4}     '.format(team, score))
            return (match_num, False) if first_team else (match_num + 1, True)
        else:
            line.append(' ' * 40)
            return (match_num, first_team)

    def _actually_print_bracket(self, lines, display):
        bracket = '\n'.join([''.join(line) for line in lines])
        if display:
            print(bracket)
        return bracket


class StandardBracket(PrintableBracket):

    """A standard bracket."""

    pass


class Cup(Bracket):

    """Base class for knockout cups."""

    def __init__(self, team_count, teams=[]):
        """Constructor.

        @param team_count: The expected number of teams
        @type team_count: int
        @param teams: The teams in this cup
        @type teams: list
        @raise ValueError: If the list of teams has the wrong number of teams
        """
        super(Cup, self).__init__()
        if not teams:
            self.teams = list(map(lambda x: 'Team ' + str(x),
                                  range(1, team_count + 1)))
        else:
            self.teams = teams
        if len(self.teams) != team_count:
            raise ValueError('Wrong number of teams')

    @property
    def team_count(self):
        """The number of teams in this cup."""
        return len(self.teams)

    def play_cup(self):
        """Play the whole cup.

        @return: The winner of the cup
        """
        try:
            while True:
                self.play_match()
        except CupFinished as e:
            return e.winner

    def update_teams(self, teams):
        """Update the list of teams and the first-round matches.

        @param teams: The new list of teams
        @type teams: list
        """
        raise NotImplementedError


class PrintableCup(Cup, PrintableBracket):

    """Combo class for a full cup printable to the console."""

    def print_cup(self, display=True):
        """Print the cup to a string and (optionally) the console.

        @param display: Whether to print to the console.
        @type display: bool
        @return: The displayed bracket
        @rtype: str
        """
        raise NotImplementedError


class StandardCup(PrintableCup):

    """A standard cup."""

    pass


class CupFinished(RuntimeError):

    """Exception for cup simulating its final match.

    This exception signals that the cup is over and that no more matches can be
    simulated. The consumer of the cup object should note the winner and move on.
    """

    def __init__(self, winner):
        """Constructor.

        @param winner: The winner of the cup
        @type winner: The type of teams in the cup
        """
        self.winner = winner


class CupConfig(object):

    """Cup configuration singleton class."""

    created = False

    def __init__(self):
        """Constructor."""
        if CupConfig.created:
            raise RuntimeError
        CupConfig.created = True
        self._cup_types = {}
        for cup in pkg_resources.iter_entry_points(group='competitions.cup.types'):
            self._cup_types.update({cup.name: cup.load()})

    def cup(self, code):
        """Retrieve the cup referred to by this code.

        @param code: The code for the cup class
        @type code: str
        @return: The cup class for the provided code.
        @rtype: Cup
        @raise KeyError: If there is no cup class loaded for this code
        """
        return self._cup_types[code]


config = CupConfig()
