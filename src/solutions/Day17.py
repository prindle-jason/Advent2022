# https://adventofcode.com/2022/day/17 
from adventutil.DataImport import InputType
from adventutil.Day import Day

YEAR, DAY = 2022, 17

EXPECTED_A = 3239
EXPECTED_B = 1594842406882
INPUT_TYPE = InputType.LIVE_DATA

class Day17(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        return self.simulate(2022)

    def partB(self):
        return self.simulate(int(1e12))
    
    def simulate(self, limit):
        jets, jet_index = self.lines[0], 0
        chamber = Day17.Chamber()
        spawner = Day17.RockSpawner()
        loop_detection_data = {}

        loop_start, loop_end = None, None
        loop_found = False
        while not loop_found:
            rock = spawner.next((2, 4 + chamber.highest))
            chamber.fit(max([cell[1] for cell in rock]))

            rock_dropped = True
            while rock_dropped:
                rock, rock_dropped = self.rock_move(rock, jets[jet_index], chamber)
                jet_index = (jet_index + 1) % len(jets)
          
            chamber.lock(rock)

            current_exposed = chamber.get_exposed()
            for start_count,(start_jet, start_height, start_exposed) in loop_detection_data.items():
                if start_jet == jet_index and start_count % 5 == spawner.count % 5 and start_exposed == current_exposed:
                    loop_start, loop_end = (start_count, start_height),(spawner.count, chamber.highest)
                    loop_found = True
                    break

            loop_detection_data[spawner.count] = (jet_index, chamber.highest, current_exposed)

        count_diff =  loop_end[0] - loop_start[0]
        height_diff = loop_end[1] - loop_start[1]

        (div, mod) = divmod(limit - loop_start[0], count_diff)
        remainder_height = loop_detection_data[loop_start[0] + mod][1]

        return div * height_diff + remainder_height

    def rock_move(self, rock, jet, chamber: 'Chamber') -> tuple:
        '''Attempts to move rock.  Returns tuple (new rock position, did-rock-drop boolean)'''
        #Attempt left/right move
        shift = 1 if jet == '>' else -1
        if chamber.is_clear(rock, (shift,0)):
            rock = [(x+shift,y) for (x,y) in rock]
        
        #Attempt to drop
        if chamber.is_clear(rock, (0, -1)):
            return [(x,y-1) for (x,y) in rock], True

        return rock, False

    class Chamber:
        '''List of list of ints'''
        def __init__(self):
            self.floors = []
            self.WIDTH = 7
            self.highest = 0
            self.floors.append([1] * self.WIDTH)

        def is_clear(self, rock, shift) -> bool:
            ''' Returns whether rock can be moved to shifted position. '''
            for sx, sy in [(rx + shift[0], ry + shift[1]) for (rx,ry) in rock]:
                if not (0 <= sx < self.WIDTH and 0 <= sy < len(self.floors) and self.get_cell(sx,sy) == 0):
                    return False
            return True

        def get_cell(self, x, y):
            return self.floors[y][x]

        def get_cell_safe(self, x, y):
            '''Checks if x,y is valid before returning.  Returns -1 if invalid'''
            if not (0 <= x < self.WIDTH and 0 <= y < len(self.floors)):
                return -1
            return self.floors[y][x]

        def lock(self, rock):
            '''Bakes a rock into the chamber'''
            for (x,y) in rock:
                if y > self.highest:
                    self.highest = y
                self.floors[y][x] = 1

        def fit(self, index):
            while len(self.floors) < index + 1:
                self.floors.append([0] * self.WIDTH)

        def get_exposed(self):
            '''Returns a set of cells in chamber that are "exposed" to air from the top '''
            start = (0, self.highest + 1) #Always start on first empty row
            need_to_check = [start]
            checked = []
            exposed = set()

            shifts = [(0,1),(0,-1),(-1,0),(1,0)] #shifts for up, down, left, right
            while need_to_check:
                (cx,cy) = need_to_check.pop()
                checked.append((cx,cy))

                for (sx,sy) in shifts:
                    px,py = (cx+sx,cy+sy)
                    if (px,py) in checked or py > self.highest + 1:
                        continue

                    element = self.get_cell_safe(px,py)
                    if element == -1:
                        continue
                    elif element:
                        exposed.add((px,self.highest-py))
                    else:
                        need_to_check.append((px,py))
            return exposed

        def print(self, limit=10):
            floors_to_print = self.floors[-1*limit:]
            for floor in floors_to_print[::-1]:
                floor = ''.join(['#' if i else '.' for i in floor])
                print(f'|{floor}|')

    class RockSpawner:
        def __init__(self):
            self.count = 0

        def next(self, root):
            '''Gets next block and increments counter.  'Root' parameter is (x,y) tuple representing bottom-left corner of block bounding box'''
            match self.count % 5:
                case 0: #flat4
                    base = [(0,0),(1,0),(2,0),(3,0)]
                case 1: #plus
                    base = [(1,0),(0,1),(2,1),(1,2)]
                case 2: #jay
                    base = [(0,0),(1,0),(2,0),(2,1),(2,2)]
                case 3: #vert4
                    base = [(0,0),(0,1),(0,2),(0,3)]
                case 4: #block
                    base = [(0,0),(1,0),(0,1),(1,1)]

            self.count += 1
            return [(cx + root[0], cy + root[1]) for (cx,cy) in base]

if __name__ == '__main__':
    Day17().run(INPUT_TYPE)
