# https://adventofcode.com/2022/day/1
from adventutil.DataImport import InputType
from adventutil.Day import Day
from adventutil.ListHelper import list_split
from adventutil.IntHelper import strings_to_int

YEAR, DAY = 2022, 1

EXPECTED_A = 68923
EXPECTED_B = 200044
INPUT_TYPE = InputType.LIVE_DATA

class Day1(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        #return max([sum(list_strings_to_int(elf)) for elf in list_split(self.lines,'')])

        max_total = 0
        for elf in list_split(self.lines,''):
            elf_total = sum(strings_to_int(elf))
            max_total = max(max_total,elf_total)
        return max_total

    def partB(self):
        elves = list_split(self.lines,'')                            
        elves = [strings_to_int(elf) for elf in elves]    
        elves = [sum(elf) for elf in elves]                         
        return sum(sorted(elves)[-3:])

if __name__ == '__main__':
    Day1().run(INPUT_TYPE)