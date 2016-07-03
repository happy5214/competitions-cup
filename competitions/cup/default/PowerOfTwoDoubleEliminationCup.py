# -*- coding: utf-8  -*-
"""Double-elimination cup for powers of two."""

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

from competitions.match import config
from competitions.cup import StandardCup, CupFinished
from competitions.cup.default.PowerOfTwoLosersBracket import PowerOfTwoLosersBracket
from competitions.cup.default.PowerOfTwoSingleEliminationCup import PowerOfTwoSingleEliminationCup


class PowerOfTwoDoubleEliminationCup(StandardCup):

    """Standard double-elimination cup for powers of two (4, 8, 16, etc.)."""

    def __init__(self, rounds=0, teams=[], require_double_win=True):
        """Constructor.

        @param rounds: The number of rounds
        @type rounds: int
        @param teams: An optional list of teams
        @type teams: list
        """
        # Parent constructor
        super(PowerOfTwoDoubleEliminationCup, self).__init__(teams=teams,
                                                             team_count=2 ** rounds)

        # Parameters
        self.require_double_win = require_double_win

        Match = config.base_match  # Load match class

        # Bracket setup
        self.winners_bracket = PowerOfTwoSingleEliminationCup(rounds=rounds,
                                                              teams=self.teams)
        self.losers_bracket = PowerOfTwoLosersBracket(rounds=rounds)
        self.bracket_progression = [self.losers_bracket, self.winners_bracket,
                                    self.losers_bracket] * (rounds - 1)
        self.current_bracket = self.winners_bracket
        self.current_bracket_index = -1
        self.final = Match('Winners Bracket Winner', 'Losers Bracket Winner')
        self.final_scores = [('', ''), ('', '')]
        self.winners = {}

    def play_match(self):
        """Play a cup match.

        @return: The winner of the simulated match
        @raise CupFinished: If the cup is finished
        """
        try:
            if self.current_bracket.round_over:
                self.current_bracket_index += 1
                self.current_bracket = self.bracket_progression[self.current_bracket_index]
            winner = self.current_bracket.play_match()
            if self.current_bracket == self.winners_bracket:
                loser = self.current_bracket.current_match.loser
                self.losers_bracket.add_team(loser)
            return winner
        except CupFinished as cf:
            self.winners[self.current_bracket] = cf.winner
            if self.current_bracket == self.winners_bracket:
                self.final.team1 = cf.winner
                loser = self.current_bracket.current_match.loser
                self.losers_bracket.add_team(loser)
            else:
                self.final.team2 = cf.winner
            return cf.winner
        except IndexError:
            winner = self.final.play()
            self.final_scores[0] = (self.final.score1, self.final.score2)
            if not self.require_double_win or winner == self.winners[self.winners_bracket]:
                self.winner = winner
                raise CupFinished(winner)
            else:
                self.winner = self.final.play()
                self.final_scores[1] = (self.final.score1, self.final.score2)
                raise CupFinished(self.winner)

    def update_teams(self, teams):
        """Update the list of teams and the first-round matches.

        @param teams: The new list of teams
        @type teams: list
        """
        self.teams = teams
        self.winners_bracket.update_teams(teams)

    def print_cup(self, display=True):
        """Print the cup to a string and (optionally) the console.

        @param display: Whether to print to the console.
        @type display: bool
        @return: The displayed bracket
        @rtype: str
        """
        winners_printout = self.winners_bracket.print_cup(display=False)
        losers_printout = self.losers_bracket.print_cup(display=False)
        final_printout = (
            '\n'
            '{:<30} {:>4} {:>4}     '
            '                                             '
            '\n'
            '                                             '
            '                                             '
            '\n'
            '{:<30} {:>4} {:>4}     '
            '                                             '
            '\n'
        ).format(self.final.team1, self.final_scores[0][0], self.final_scores[1][0],
                 self.final.team2, self.final_scores[0][1], self.final_scores[1][1])
        full_printout = winners_printout + losers_printout + '\n' + final_printout
        if display:
            print(full_printout)
        return full_printout
