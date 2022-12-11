# https://adventofcode.com/2022/day/2
from enum import Enum

from adventutil.DataImport import InputType
from adventutil.Day import Day

YEAR = 2022
DAY  = 2

EXPECTED_A = 10624
EXPECTED_B = 14060
INPUT_TYPE = InputType.LIVE_DATA

#List orders are (Rock,Paper,Scissor) or (Lose,Draw,Win) where applicable
selections          = ['R','P','S']
crypticPrimary      = ['A','B','C']
crypticSecondary    = ['X','Y','Z']

outcomes            = ['L','D','W']
scores              = [  0,  3,  6]

class Day2(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        total = 0
        for line in self.lines:
            opponent_selection = self.decrypt_opponent(line[0])
            own_selection = self.decrypt_own(line[2])
            outcome = self.determine_outcome(opponent_selection,own_selection)

            total += self.calc_score(own_selection, outcome)
            
        return total

    def partB(self):
        total = 0
        for line in self.lines:
            opponent_selection = self.decrypt_opponent(line[0])
            outcome = self.decrypt_outcome(line[2])
            own_selection = self.determine_selection(opponent_selection, outcome)

            total += self.calc_score(own_selection, outcome)
            
        return total

    def calc_score(self, own_selection, outcome):
        score = scores[outcomes.index(outcome)]
        bonus = selections.index(own_selection)+1

        return score + bonus

    def decrypt_opponent(self,opp):
        return selections[crypticPrimary.index(opp)]

    def decrypt_own(self,own):
        return selections[crypticSecondary.index(own)]

    def decrypt_outcome(self,outcome):
        return outcomes[crypticSecondary.index(outcome)]

    def determine_outcome(self,opponent_selection,own_selection):
        winning_selection = self.winning_selection(opponent_selection)
        return 'W' if own_selection == winning_selection else 'D' if own_selection == opponent_selection else 'L'

    def determine_selection(self,opponent_selection,outcome):
        return self.winning_selection(opponent_selection) if outcome == outcomes[2] else opponent_selection if outcome == outcomes[1] else self.losing_selection(opponent_selection)

    def winning_selection(self,opponent_selection):
        return selections[(selections.index(opponent_selection) + 1) % 3]

    def losing_selection(self,opponent_selection):
        return selections[(selections.index(opponent_selection) + 2) % 3]
    
if __name__ == '__main__':
    Day2().run(INPUT_TYPE)
