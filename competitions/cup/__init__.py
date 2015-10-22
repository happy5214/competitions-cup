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


class Cup(object):

    """Base class for knockout cups."""

    def __init__(self, team_count, teams=[]):
        """Constructor.

        @param team_count: The expected number of teams
        @type team_count: int
        @param teams: The teams in this cup
        @type teams: list
        @raise ValueError: If the list of teams has the wrong number of teams
        """
        self.winner = None
        self.matches = []
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

    def play_match(self):
        """Play a cup match.

        @return: The winner of the simulated match
        @raise CupFinished: If the cup is finished
        """
        raise NotImplementedError

    def update_teams(self, teams):
        """Update the list of teams and the first-round matches.

        @param teams: The new list of teams
        @type teams: list
        """
        raise NotImplementedError

    def print_cup(self, display=True):
        """Print the cup to a string and (optionally) the console.

        @param display: Whether to print to the console.
        @type display: bool
        @return: The displayed bracket
        @rtype: str
        """
        raise NotImplementedError


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
