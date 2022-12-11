# https://adventofcode.com/2022/day/1
from adventutil.DataImport import InputType
from adventutil.Day import Day
from adventutil.ListHelper import list_split

YEAR, DAY = 2022, 1

EXPECTED_A = 68923
EXPECTED_B = 200044
INPUT_TYPE = InputType.LIVE_DATA

class Day1(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        elves = list_split(self.lines,'')         
        elves = [[int(e) for e in elf] for elf in elves]            # Convert elements to int       
        return max([sum(elf) for elf in elves])                     # Return max sum

    def partB(self):
        elves = list_split(self.lines,'')                           # Get input, split on empty lines        
        elves = [[int(e) for e in elf] for elf in elves]            # Convert elements to int    
        elves = [sum(elf) for elf in elves]                         # Sum each elf
        elves.sort()
        return sum(elves[-3:])

if __name__ == '__main__':
    Day1().run(INPUT_TYPE)