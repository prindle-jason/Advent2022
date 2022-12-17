# https://adventofcode.com/2022/day/3
from adventutil.DataImport import InputType
from adventutil.Day import Day

YEAR, DAY = 2022, 3

EXPECTED_A = 7863
EXPECTED_B = 2488
INPUT_TYPE = InputType.LIVE_DATA

class Day3(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        sum = 0
        for line in self.lines:
            half_len = len(line)//2
            comps = [line[:half_len],line[half_len:]]

            for c in comps[0]:
                if c in comps[1]:
                    sum += self.__get_ascii_value(c)
                    break

        return sum

    def partB(self):
        sum = 0

        #split lines into groups of 3
        start_indices = range(0,len(self.lines),3)
        for group in [self.lines[i:i+4] for i in start_indices]:

            for c in group[0]:
                if c in group[1] and c in group[2]:
                    sum += self.__get_ascii_value(c)
                    break

            group.clear()

        return sum

    def __get_ascii_value(self,match):
        return ord(match) - (96 if match.islower() else 38)       

if __name__ == '__main__':
    Day3().run(INPUT_TYPE)
