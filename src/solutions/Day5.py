# https://adventofcode.com/2022/day/5
from adventutil.DataImport import InputType
from adventutil.Day import Day
from adventutil.IntHelper import string_to_ints

from collections import deque
from itertools import product

YEAR = 2022
DAY  = 5

EXPECTED_A = "HNSNMTLHQ"
EXPECTED_B = "RNLFDJMCT"
INPUT_TYPE = InputType.LIVE_DATA

STACK_COUNT = 9
MAX_HEIGHT = 8
STARTING_OP_INDEX = 10

class Day5(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):    
        stacks = self.build_stacks(self.lines[:MAX_HEIGHT+1])
        ops = self.build_operations(self.lines[STARTING_OP_INDEX:])

        for op in ops:
            count, _from, _to = op#op[0], op[1], op[2]
            for _ in range(count):                
                stacks[_to-1].append(stacks[_from-1].pop())

        return ''.join([stack.pop() for stack in stacks])

    def partB(self):
        stacks = self.build_stacks(self.lines[:MAX_HEIGHT+1])
        ops = self.build_operations(self.lines[STARTING_OP_INDEX:])

        for op in ops:
            count, from_stack, to_stack = op
            
            bundle = [stacks[from_stack-1].pop() for _ in range(count)]
            stacks[to_stack-1].extend(reversed(bundle))

        return ''.join([stack.pop() for stack in stacks])

    def build_stacks(self, lines):
        stacks = [deque() for _ in range(STACK_COUNT)]

        for row, column in product(range(MAX_HEIGHT),range(STACK_COUNT)):
            target = lines[row][4*column+1]
            if target.strip():
                stacks[column].appendleft(target)

        return stacks

    def build_operations(self, lines):
        return [string_to_ints(line) for line in lines]

if __name__ == '__main__':
    Day5().run(INPUT_TYPE, False)
