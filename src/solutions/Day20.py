# https://adventofcode.com/2022/day/20
from adventutil.DataImport import InputType
from adventutil.Day import Day

YEAR, DAY = 2022, 20

EXPECTED_A = 7225
EXPECTED_B = 548634267428
INPUT_TYPE = InputType.LIVE_DATA

class Day20(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        lines = self.lines.copy()
        for index, line in enumerate(lines):
            lines[index] = (int(line), index)

        lines = self.decrypt(lines)            
        return self.find_coordinates(lines)

    def partB(self):
        DECRYPT_KEY = 811589153
        DECRYPT_COUNT = 10

        lines = self.lines.copy()
        for index, line in enumerate(lines):
            lines[index] = (int(line)*DECRYPT_KEY, index)

        for _ in range(DECRYPT_COUNT):
            lines = self.decrypt(lines)
            
        return self.find_coordinates(lines)

    def decrypt(self, lines):
        for next_index_to_move in range(len(lines)):
            for search_index, (sv, si) in enumerate(lines):
                if si == next_index_to_move:
                    current_index, current_value, original_index = search_index, sv, si
                    break

            new_index = (current_index + current_value) % (len(lines)-1)

            lines = lines[:current_index] + lines[current_index+1:]
            lines = lines[:new_index] + [(current_value, original_index)] + lines[new_index:]
        return lines

    def find_coordinates(self, lines):
        zero_index = None
        for index, (lv, _) in enumerate(lines):
            if lv == 0:
                zero_index = index
                break

        total = 0
        for x in (1000, 2000, 3000):
           total += lines[(x+zero_index) % len(lines)][0]
        return total

if __name__ == '__main__':
    Day20().run(INPUT_TYPE)
