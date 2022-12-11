# https://adventofcode.com/2022/day/3
from adventutil.DataImport import InputType
from adventutil.Day import Day

YEAR = 2022
DAY  = 3

EXPECTED_A = 7863
EXPECTED_B = 2488
INPUT_TYPE = InputType.LIVE_DATA

class Day3(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        sum = 0
        for line in self.lines:
            comps = [line[:len(line)//2],line[len(line)//2:]]

            for c in comps[0]:
                if c in comps[1]:
                    sum += self.__get_ascii_value(c)
                    break

        return sum

    def partB(self):

        sum = 0
        for x in range(0, len(self.lines),3):
            comps = self.lines[x:x+3]

            for c in comps[0]:
                if c in comps[1] and c in comps[2]:
                    sum += self.__get_ascii_value(c)
                    break

        return sum

    def __get_ascii_value(self,match):
        return ord(match) - (96 if match.islower() else 38)       

if __name__ == '__main__':
    Day3().run(INPUT_TYPE)
