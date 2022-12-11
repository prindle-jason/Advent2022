# https://adventofcode.com/2022/day/9
# Refactored code shamelessly inspired by:
''' https://topaz.github.io/paste/#XQAAAQDYAQAAAAAAAAA5G8pm5rq2zGEq3FAnMmnq8EER0UoD/ZrEuZHeyNjL79bpZLXfg/
    Dbz424aybsPDyjUN1dpuHMGZn4ncEbddEKyH1V5oJxNIugTQYA3a0cg3tPo+1+xICju6pge5dxTN1gMMRkxmRSnVmqaS4/mppv4aO
    0g0/4qq8pDfs+1MMhAxsKcMsZLfoW/sMz8uQSt8wUrld9CbEbjBoMIwyvn2iz+zHG+akaQtqO2OKeZImV4dvBK/c74Xb2Y0LE8oQb
    z+gXadim+4L9LIw7aJHgJ/PbYZ0XkaiqhSa8GHdRwosEbaQ9Q8YjWhAlGlThJfLj9Tf7CqDCASr/xFWvTuAlOrdqb5EhjNdtJ+joN
    XcFJ2wTAqQ4X/RFVi7/7cYS+A=='''

from adventutil.DataImport import InputType
from adventutil.Day import Day
from adventutil.Compare import compare

YEAR = 2022
DAY  = 9

EXPECTED_A = 5878
EXPECTED_B = 2405
INPUT_TYPE = InputType.LIVE_DATA

COMMAND_MOVE = {'U': +1j, 'D': -1j, 'L': -1, 'R': +1}

follow_move = lambda lead, follow : complex(compare(lead.real,follow.real) + 1j*compare(lead.imag,follow.imag))

class Day9(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        return self._simulate_rope(2)

    def partB(self):
        return self._simulate_rope(10)

    def _simulate_rope(self,rope_length):
        rope = [complex()] * rope_length

        tail_positions = set()
        tail_positions.add(rope[rope_length-1])
        for command in [line.split() for line in self.lines]:
            for step in range(int(command[1])):
                rope[0] += COMMAND_MOVE[command[0]]

                for knot in range(rope_length-1):
                    if abs(rope[knot]-rope[knot+1]) >= 2:
                        rope[knot+1] += follow_move(rope[knot],rope[knot+1])

                tail_positions.add(rope[rope_length-1])
        return len(tail_positions)

if __name__ == '__main__':
    Day9().run(INPUT_TYPE)
