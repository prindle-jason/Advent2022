# https://adventofcode.com/2022/day/14
from enum import Enum

from adventutil.DataImport import InputType
from adventutil.Day import Day
from adventutil.IntHelper import strings_to_ints

YEAR, DAY = 2022, 14

EXPECTED_A = 799
EXPECTED_B = 29076
INPUT_TYPE = InputType.LIVE_DATA

class Day14(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        scan = Scan(self.lines, False) 

        count = 0
        while scan.next():
            count += 1

        #print(scan)
        return count

    def partB(self):
        scan = Scan(self.lines, True)

        count = 0
        while scan.next():
            count += 1
        #print(scan)
        return count + 1

class Scan():
    def __init__(self, lines, is_expandable : bool):
        self._scan = {}     
        self._expandable = is_expandable
        
        self.__build_scan(lines)
        self._bounds = self.__find_bounds(is_expandable)

    def __build_scan(self, lines):
        input = strings_to_ints(lines)
        self.set(500, 0, Legend.SOURCE)
        for line in input:
            while len(line) > 2:
                x1, y1, x2, y2 = line[0:4]
                line = line[2:]

                for new_x in range(min(x2,x1),max(x2,x1)+1):
                    self.set(new_x, y1, Legend.ROCK)
                for new_y in range(min(y2,y1),max(y2,y1)+1):
                    self.set(x1, new_y, Legend.ROCK)

    def __find_bounds(self, is_expandable):
        min_x = min([min([key for key in self._scan[row]]) for row in self._scan])
        max_x = max([max([key for key in self._scan[row]]) for row in self._scan])
        min_y = min([row for row in self._scan])
        max_y = max([row for row in self._scan]) + (1 if is_expandable else 0)

        return [min_x, max_x, min_y, max_y]

    def get(self, x, y):
        if y in self._scan and x in self._scan[y]:
            return self._scan[y][x]
        return Legend.AIR

    def set(self, x, y, value):
        if y not in self._scan:
            self._scan[y] = {}
        self._scan[y][x] = value

    def next(self):
        source = [500, 0]
        search =  source.copy()
        
        while True:
            next = None
            for dx in [0,-1, +1]:                   
                sx, sy = search[0] + dx, search[1] + 1
                search_value = self.get(sx,sy)

                if not self._expandable:       #Part A logic
                    if sx < self._bounds[0] or sx > self._bounds[1] or sy < self._bounds[2] or sy > self._bounds[3]:
                        return False
                else:                           #Part B logic
                    if sx < self._bounds[0]:  self._bounds[0] = sx
                    if sx > self._bounds[1]:  self._bounds[1] = sx

                    if search_value == Legend.AIR and sy == self._bounds[3]:
                        self.set(sx, sy, Legend.SAND)
                        return True

                if self.get(sx, sy) == Legend.AIR:
                    next = [sx, sy]
                    break   

            if not next:
                if search == source:
                    return False
                self.set(search[0], search[1], Legend.SAND)
                return True 
            search = next
    
    def __repr__(self):
        lines = []

        for row in range(self._bounds[2],self._bounds[3]+1):
            line = '.' * (self._bounds[1]-self._bounds[0]+1)
            if row in self._scan:
                row_dict = self._scan[row]
                for k,v in row_dict.items():
                    line = line[:k - self._bounds[0]] + v.value + line[k - self._bounds[0]+1:]
            lines.append(line)
        return '\n'.join(lines)

class Legend(Enum):
    ROCK = '#'
    AIR  = '.'
    SAND = 'o'
    SOURCE = '+'

if __name__ == '__main__':
    Day14().run(INPUT_TYPE)
