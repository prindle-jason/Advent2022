# https://adventofcode.com/2022/day/5
from adventutil.DataImport import InputType
from adventutil.Day import Day

YEAR = 2022
DAY  = 5

EXPECTED_A = "HNSNMTLHQ"
EXPECTED_B = "RNLFDJMCT"
INPUT_TYPE = InputType.LIVE_DATA

STACK_COUNT = 9
MAX_STARTING_STACK = 8
STARTING_OP_INDEX = 10

class Day5(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):    
        stacks = self.__build_stacks(self.lines[:MAX_STARTING_STACK+1])
        ops = self.__build_ops(self.lines[STARTING_OP_INDEX:])

        for op in ops:
            count, from_index, to_index = op[0], op[1], op[2]
            for c in range(count):                
                stacks[to_index].append(stacks[from_index].pop())

        return ''.join([stack.pop() for stack in stacks])

    def partB(self):
        stacks = self.__build_stacks(self.lines[:MAX_STARTING_STACK+1])
        ops = self.__build_ops(self.lines[STARTING_OP_INDEX:])

        for op in ops:
            count, from_index, to_index = op[0], op[1], op[2]

            stacks[to_index].extend(stacks[from_index][-1*count:])
            stacks[from_index] = stacks[from_index][:-1*count]

        return ''.join([stack.pop() for stack in stacks])

    def __build_stacks(self, lines):
        stacks = [[] for _ in range(STACK_COUNT)]

        for row in range(MAX_STARTING_STACK):
            for column in range(STACK_COUNT):
                target = lines[row][4*column+1]
                if target != ' ':
                    stacks[column].insert(0,target)

        return stacks

    def __build_ops(self, lines):
        ops = []
        for op in lines:
            op = op.split(' ')[1::2]   #split and only keep indices 1,3,5
            op = [int(i) for i in op]

            op[1] -= 1
            op[2] -= 1

            ops.append(op)
        return ops

if __name__ == '__main__':
    Day5().run(INPUT_TYPE, False)
