# https://adventofcode.com/2022/day/10
from adventutil.DataImport import InputType
from adventutil.Day import Day

YEAR, DAY = 2022, 10

EXPECTED_A = 13180
EXPECTED_B = True
B_OUTPUT = '''####.####.####..##..#..#...##..##..###..
#.......#.#....#..#.#..#....#.#..#.#..#.
###....#..###..#....####....#.#..#.###..
#.....#...#....#....#..#....#.####.#..#.
#....#....#....#..#.#..#.#..#.#..#.#..#.
####.####.#.....##..#..#..##..#..#.###..'''
INPUT_TYPE = InputType.LIVE_DATA
#INPUT_TYPE = InputType.SAMPLE_DATA

class Day10(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        self.cycle, self.signal, self.x = 0, 0, 1

        for command in [line.split() for line in self.lines]:
            self.tickA()
            if command[0] == 'addx':
                self.tickA()
                self.x += int(command[1])
        return self.signal

    def tickA(self):
        self.cycle += 1
        if self.cycle in range(20,221,40):
            self.signal += self.cycle*self.x

    def partB(self):
        self.cycle, self.x = 0, 1
        self.screen = []
        self.crt_line = ''

        for command in [line.split() for line in self.lines]:
            self.tickB()
            if command[0] == 'addx':
                self.tickB()
                self.x += int(command[1])      

        return B_OUTPUT == '\n'.join(self.screen)

    def tickB(self):
        self.cycle += 1

        sprite_range = range(self.x,self.x+3)
        current_pixel = self.cycle % 40 if self.cycle % 40 != 0 else 40
        self.crt_line += '#' if current_pixel in sprite_range else '.'
        
        if len(self.crt_line) % 40 == 0:
            self.screen.append(self.crt_line)
            self.crt_line = ''

if __name__ == '__main__':
    Day10().run(INPUT_TYPE)
