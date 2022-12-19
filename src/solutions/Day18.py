# https://adventofcode.com/2022/day/18
from itertools import product
from adventutil.DataImport import InputType
from adventutil.Day import Day
from adventutil.IntHelper import strings_to_ints
YEAR, DAY = 2022, 18

EXPECTED_A = 3326
EXPECTED_B = 1996
INPUT_TYPE = InputType.LIVE_DATA

FACE_NEIGHBOR_OFFSETS = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]]

class Day18(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        lava = [tuple(lst) for lst in strings_to_ints(self.lines)]
        return self.count_exposed_faces(lava)

    def partB(self):
        lava_cubes = [tuple(lst) for lst in strings_to_ints(self.lines)]

        border_cubes = self.generate_borders(lava_cubes)
        border_groups = self.group_borders(border_cubes)
        border_groups.remove(self.find_exterior_group(border_groups))

        all_exposure = self.count_exposed_faces(lava_cubes)
        inner_exposure = self.count_inner_exposed_faces(lava_cubes, border_groups)

        return all_exposure - inner_exposure

    def count_exposed_faces(self, cubes):
        total = 0
        for cube in cubes:
            exposed = 6
            for offset in FACE_NEIGHBOR_OFFSETS:
                neighbor = tuple([c+o for c,o in zip(cube,offset)])
                if neighbor in cubes:
                    exposed -= 1
            total += exposed
        return total

    def count_inner_exposed_faces(self, lava_cubes, interior_groups):
        inner_exposure = 0
        for group in interior_groups:
            for cube in group:
                exposed = 0
                for offset in FACE_NEIGHBOR_OFFSETS:
                    neighbor = tuple([x+y for x,y in zip(cube, offset)])
                    if neighbor in lava_cubes:
                        exposed += 1
                inner_exposure += exposed
        return inner_exposure

    def find_exterior_group(self, border_groups):
        exterior_group, min_x = None, -1
        for group in border_groups:
            for (x,_,_) in group:
                if min_x == -1 or x < min_x:
                    min_x = x
                    exterior_group = group

        return exterior_group

    def generate_borders(self, lava_cubes):
        border_cubes = set()
        for lava in lava_cubes:
            offsets = self.all_offsets()
            for offset in offsets:
                target = tuple([x+y for x,y in zip(lava, offset)])
                if target not in lava_cubes:
                    border_cubes.add(target)
        return border_cubes

    def group_borders(self, border_cubes : set[tuple]):
        groups = []

        while border_cubes:
            group = [border_cubes.pop()]

            for cube in group:
                for offset in FACE_NEIGHBOR_OFFSETS:
                    target = tuple([x+y for x,y in zip(cube, offset)])

                    if target in border_cubes:
                        group.append(target)
                        border_cubes.remove(target)
            groups.append(group)

        return groups

    def all_offsets(self):
        '''Returns the 26 3D offsets surrounding (0,0,0)'''
        offsets = list(product([-1,0,1],[-1,0,1],[-1,0,1]))
        offsets.remove((0,0,0))
        return offsets

if __name__ == '__main__':
    Day18().run(INPUT_TYPE)
