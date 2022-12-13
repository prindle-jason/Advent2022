# https://adventofcode.com/2022/day/4
from adventutil.DataImport import InputType
from adventutil.Day import Day
from adventutil.IntHelper import string_to_ints

YEAR = 2022
DAY  = 4

EXPECTED_A = 448
EXPECTED_B = 794
INPUT_TYPE = InputType.LIVE_DATA

class Day4(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        count = 0
        for line in self.lines:            
            values = string_to_ints(line)    
            if values[0] >= values[2] and values[1] <= values[3]:
                count += 1
            elif values[0] <= values[2] and values[1] >= values[3]:
                count += 1

        return count

    def partB(self):        
        count = 0
        for line in self.lines:
            values = string_to_ints(line) 
                    
            for x in range(values[0], values[1]+1):
                if values[2] <= x <= values[3]:
                    count += 1
                    break

        return count

if __name__ == '__main__':
    Day4().run(INPUT_TYPE)
