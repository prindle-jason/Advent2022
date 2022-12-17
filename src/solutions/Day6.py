# https://adventofcode.com/2022/day/6
from adventutil.DataImport import InputType
from adventutil.Day import Day

YEAR, DAY = 2022, 6

EXPECTED_A = 1892
EXPECTED_B = 2313
INPUT_TYPE = InputType.LIVE_DATA

class Day6(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        return self.__find_marker(self.lines[0],4)

    def partB(self):
        return self.__find_marker(self.lines[0],14)

    def __find_marker(self,line,size):
        for x in range(len(line)):
            if len(set(line[x:x+size])) == size:
                return x+size

if __name__ == '__main__':
    Day6().run(INPUT_TYPE)
