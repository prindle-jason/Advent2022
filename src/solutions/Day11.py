# https://adventofcode.com/2022/day/11
from dataclasses import dataclass
from functools import reduce
from operator import mul
import re

from adventutil.DataImport import InputType
from adventutil.Day import Day
from adventutil.ListHelper import list_split

YEAR, DAY = 2022, 11

EXPECTED_A = 66802
EXPECTED_B = 21800916620
INPUT_TYPE = InputType.LIVE_DATA

get_ints = lambda s : [int(i) for i in re.findall('\d+', s)]

class Day11(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        return self.simulate(20,3)

    def partB(self):
        return self.simulate(10000,1)

    def simulate(self,rounds,worry_div):
        monkeys = self.generate_monkeys(worry_div)
        lcm = reduce(mul, [monkey.test[0] for monkey in monkeys])

        for round in range(rounds):
            for monkey in monkeys:
                while len(monkey.items) > 0:                    
                    target, worry = monkey.inspect(lcm)
                    monkeys[target].items.append(worry)

        counts = sorted([monkey.count for monkey in monkeys])
        return counts[-2]*counts[-1]

    def generate_monkeys(self,worry_div):
        monkeys = []
        for input in list_split(self.lines,''):
            monkeys.append(self.generate_monkey(input,worry_div))
        return monkeys

    def generate_monkey(self,input,worry_div):
        id    = get_ints(input[0])[0]
        items = get_ints(input[1])
        op = input[2].split()[-2:]
        test  = get_ints(''.join(input[3:6]))
        return Day11.Monkey(id,items,op,test,worry_div)

    @dataclass
    class Monkey:
        id : int
        items : list
        op : list
        test : list
        worry_div : int
        _count : int = 0

        @property
        def count(self):
            return self._count

        def inspect(self, lcm):
            self._count += 1
            worry = self.items[0]
            self.items.remove(worry)

            match self.op:
                case '*','old': worry *= worry
                case '+','old': worry += worry
                case '*', num : worry *= int(num)
                case '+', num : worry += int(num)

            worry = worry//self.worry_div % lcm
            target = self.test[1] if worry % self.test[0] == 0 else self.test[2]
            return target, worry

if __name__ == '__main__':
    Day11().run(INPUT_TYPE)
