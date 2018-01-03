# -*- coding: utf-8  -*-
"""Double-elimination cup for powers of two."""

# Copyright (C) 2016, 2017 Alexander Jones
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

from competitions.cup import StandardCup, StandardBracket, CupFinished, init_nested_list
from competitions.cup.default.single_elimination import PowerOfTwoSingleEliminationCup


class PowerOfTwoDoubleEliminationCup(StandardCup):

    """Standard double-elimination cup for powers of two (4, 8, 16, etc.)."""

    def __init__(self, match_class, rounds=0, teams=[], require_double_win=True):
        """Constructor.

        @param rounds: The number of rounds
        @type rounds: int
        @param teams: An optional list of teams
        @type teams: list
        """
        # Parent constructor
        super(PowerOfTwoDoubleEliminationCup, self).__init__(match_class=match_class,
                                                             teams=teams,
                                                             team_count=2 ** rounds,
                                                             rounds=rounds)

        # Parameters
        self.require_double_win = require_double_win

    def _build_bracket(self):
        """Build the bracket."""
        Match = self.MatchClass
        rounds = self.round_count
        self.winners_bracket = PowerOfTwoSingleEliminationCup(match_class=Match,
                                                              rounds=rounds,
                                                              teams=self.teams)
        self.losers_bracket = PowerOfTwoLosersBracket(match_class=Match, rounds=rounds)
        self.bracket_progression = [self.losers_bracket, self.winners_bracket,
                                    self.losers_bracket] * (rounds - 1)
        self.current_bracket = self.winners_bracket
        self.current_bracket_index = -1
        self.final = Match('Winners Bracket Winner', 'Losers Bracket Winner')
        self.final_scores = [('', ''), ('', '')]
        self.winners = {}

    def _play_match(self):
        """Play a match. Internal code."""
        if self.current_bracket.round_over:
            self.current_bracket_index += 1
            self.current_bracket = self.bracket_progression[self.current_bracket_index]
        winner = self.current_bracket.play_match()
        if self.current_bracket == self.winners_bracket:
            loser = self.current_bracket.current_match.loser
            self.losers_bracket.add_team(loser)
        return winner

    def _bracket_finished(self, cf):
        """Handle a finished sub-bracket."""
        self.winners[self.current_bracket] = cf.winner
        if self.current_bracket == self.winners_bracket:
            self.final.team1 = cf.winner
            loser = self.current_bracket.current_match.loser
            self.losers_bracket.add_team(loser)
        else:
            self.final.team2 = cf.winner
        return cf.winner

    def _play_final(self):
        """Play the cup final."""
        winner = self.final.play()
        self.final_scores[0] = (self.final.score1, self.final.score2)
        if not self.require_double_win or winner == self.winners[self.winners_bracket]:
            self.winner = winner
            raise CupFinished(winner)
        else:
            self.winner = self.final.play()
            self.final_scores[1] = (self.final.score1, self.final.score2)
            raise CupFinished(self.winner)

    def play_match(self):
        """Play a cup match.

        @return: The winner of the simulated match
        @raise CupFinished: If the cup is finished
        """
        try:
            return self._play_match()
        except CupFinished as cf:
            return self._bracket_finished(cf)
        except IndexError:
            self._play_final()

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


class PowerOfTwoLosersBracket(StandardBracket):

    """Double-elimination cup losers bracket for powers of two (4, 8, 16, etc.)."""

    def __init__(self, match_class, rounds=0):
        """Constructor.

        @param rounds: The number of rounds in the corresponding winners bracket
        @type rounds: int
        """
        super(PowerOfTwoLosersBracket, self).__init__(match_class=match_class)

        # Parameter validation
        if rounds < 2:
            raise ValueError('Not enough rounds.')

        # Object constants
        self.winners_round_count = rounds
        self.phases = rounds - 1
        self.round_count = self.phases * 2

        # Build bracket
        self._build_bracket()

        # Determine placements for losers
        self._generate_loser_placements()

    def _build_bracket(self):
        """Build the nested list representing the bracket."""
        Match = self.MatchClass
        rounds = self.winners_round_count

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
            match_count //= 2
            round = []
            for ___ in range(match_count):
                round.append(Match('Match L{} Winner'.format(losers_match_num),
                                   'Match L{} Winner'.format(losers_match_num + 1)))
                losers_match_num += 2
            self.matches.append(round)
        del self.matches[-1]

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

    def _assign_winner(self, winner):
        """Assign winner to their next match."""
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

    def _generate_layout(self):
        """Generate the bracket layout for display."""
        space = (None, None)
        first = 2 ** (self.phases - 1)
        line_count = first * 5 - 1
        layout = init_nested_list(line_count)
        first_team = True
        match_gen = self._match_for_layout
        for phase in range(self.phases):
            first = 2 ** (self.phases - 1)
            match_num = 0
            round = phase * 2
            div = 2 * 2 ** phase
            for i in range(first):
                layout[i].append(space)
            for i in range(first, line_count):
                (conf, layout_entry) = match_gen(((i - first) % div == 0),
                                                 round, match_num, first_team)
                layout[i].append(layout_entry)
                (match_num, first_team) = conf
            # Major round
            match_num = 0
            first -= 2 ** phase
            round += 1
            for i in range(first):
                layout[i].append(space)
            for i in range(first, line_count):
                try:
                    (conf, layout_entry) = match_gen(((i - first) % div == 0),
                                                     round, match_num, first_team)
                    layout[i].append(layout_entry)
                    (match_num, first_team) = conf
                except IndexError:
                    layout[i].append(space)
        return layout
