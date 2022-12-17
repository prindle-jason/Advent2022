# https://adventofcode.com/2022/day/12
from adventutil.DataImport import InputType
from adventutil.Day import Day
from adventutil.GridHelper import get_string_grid

YEAR, DAY = 2022, 12

EXPECTED_A = 481
EXPECTED_B = 480
INPUT_TYPE = InputType.LIVE_DATA

class Day12(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        self.height_grid = get_string_grid(self.lines)

        #This will track the fastest number of steps to each tile on the grid ('Start' will be zero)
        self.route_grid  = [[-1]*len(self.height_grid[0]) for _ in range(len(self.height_grid))]

        #Start and End tiles are saved then replaced with their elevations.  S -> a; E -> z
        start, end = [],[]
        for row in range(len(self.height_grid)):
            for cell in range(len(self.height_grid[0])):
                if self.height_grid[row][cell] == 'S':
                    self.height_grid[row][cell] = 'a'
                    self.route_grid[row][cell] = 0
                    start = [row,cell]
                if self.height_grid[row][cell] == 'E':
                    self.height_grid[row][cell] = 'z'
                    end = [row,cell]

        navigate_from = []
        navigate_from.append(start)

        while len(navigate_from) > 0:
            next = navigate_from[0]
            navigate_from = navigate_from[1:]

            y, x = next[0],next[1]

            #Check all directions
            directions = [[y-1,x],[y+1,x],[y,x-1],[y,x+1]]  #Up, Down, Left, Right

            for d in directions:
                y2, x2 = d[0], d[1]
                if self.should_traverse(y,x,y2,x2):
                    if [y2,x2] not in navigate_from: #Do I need this check?
                        navigate_from.append([y2,x2])
                    self.route_grid[y2][x2] = self.route_grid[y][x]+1

        #  Print route grid
        #for row in self.route_grid:
        #    print(''.join([f"{cell:03} " for cell in row]) + '\n')
        
        return self.route_grid[end[0]][end[1]]

    def should_traverse(self,y1,x1,y2,x2):
        '''determine if traversing from current to target is worthwhile'''
        # Make sure target is valid
        if y2 < 0 or y2 >= len(self.height_grid) or x2 < 0 or x2 >= len(self.height_grid[0]):
            return False

        steps1 = self.route_grid[y1][x1]
        steps2 = self.route_grid[y2][x2]

        # If next steps is -1, I've never been there, so always proceed
        if steps2 != -1 and steps2 <= steps1 + 1:
            return False

        height1 = self.height(y1,x1)
        height2 = self.height(y2,x2)

        if height2 > height1 + 1:
            return False

        return True

    def partB(self):
        self.height_grid = get_string_grid(self.lines)

        #This will track the fastest number of steps to each tile on the grid ('a' will be zero)
        self.route_grid  = [[-1]*len(self.height_grid[0]) for _ in range(len(self.height_grid))]

        #End tile and all starts are saved then replaced with their elevations.  S -> a; E -> z
        navigate_from, end  = [],[]
        for row in range(len(self.height_grid)):
            for cell in range(len(self.height_grid[0])):
                if self.height_grid[row][cell] == 'S':
                    self.height_grid[row][cell] = 'a'

                if self.height_grid[row][cell] == 'E':
                    self.height_grid[row][cell] = 'z'
                    end = [row,cell]

                if self.height_grid[row][cell] == 'a':
                    self.route_grid[row][cell] = 0
                    navigate_from.append([row,cell])
                    
        while len(navigate_from) > 0:
            next = navigate_from[0]
            navigate_from = navigate_from[1:]

            y, x = next[0],next[1]

            directions = [[y-1,x],[y+1,x],[y,x-1],[y,x+1]] 
            for d in directions:
                y2, x2 = d[0], d[1]
                if self.should_traverse(y,x,y2,x2):
                    if [y2,x2] not in navigate_from:
                        navigate_from.append([y2,x2])
                    self.route_grid[y2][x2] = self.route_grid[y][x]+1

        #Print route grid
        #for row in self.route_grid:
        #    print(''.join([f"{cell:03} " for cell in row]) + '\n')
        return self.route_grid[end[0]][end[1]]






    # From current position
        # Check all directions
            # If I can go that direction (and haven't been there faster!)
                # Add position to need_to_visit list (set?)
                # Update that position on paths map with steps + 1
        # Now traverse from each updated position


    # def partA(self):
    #     self.sanity = 0
    #     self.grid = get_string_grid(self.lines)
    #     self.paths = [[-1]*len(self.grid[0]) for _ in range(len(self.grid))]
    #     #print(self.paths)
    #     #self.paths = [[-1] for _ in range(len(self.grid[0])) * len(self.grid)] #Fastest count to each tile
        
        
    #     self.start, self.end = [],[]
    #     for row in range(len(self.grid)):
    #         for cell in range(len(self.grid[0])):
    #             if self.grid[row][cell] == 'S':
    #                 self.grid[row][cell] = 'a'
    #                 self.start = [row,cell]
    #             if self.grid[row][cell] == 'E':
    #                 self.grid[row][cell] = 'z'
    #                 self.end = [row,cell]
    #     #print(grid)
    #     visited = set()
    #     visited.add(','.join([str(i) for i in self.start]))
    #     result = self.traverse(self.start, visited, 0)
    #     #[print(path) for path in self.paths]
    #     return result

    # def traverse(self, pos, visited_tiles, steps):
    #     self.sanity += 1
    #     if self.sanity % 1000000 == 0:
    #         print(self.sanity)

    #     y, x = pos[0],pos[1]
    #     fastest = self.paths[y][x]

    #     #Update fastest route grid or abort if we've been here faster/same speed

    #     if fastest > -1:
    #         #We've been here before, let's get out!
    #         if fastest <= steps:
    #             return -1
    #         #else:
    #             #In this case, I shouldn't need to renavigate, the best from this square could be reduced by fastest-steps
    #             #Unfortunately, I'm not tracking "best from this square currently"
    #             #self.paths[y][x] = steps
    #             #return -1

    #     #if fastest == -1: #We've never been here before
    #     self.paths[y][x] = steps
    #     #elif fastest <= steps: #We've been here faster
    #     #    return -1
    #     if pos == self.end:  #We've reached the end!
    #         #print(f"Found E at {steps} count.  Visited size: {len(visited_tiles)}")
    #         return steps

    #     #Can't abort early, consider a step in the 4 directions
    #     steps += 1
    #     current = self.height(y, x)
    #     curr_str = ','.join([str(i) for i in pos])
    #     visited_tiles.add(curr_str)

    #     down  = ','.join([str(y+1),str(x)])
    #     right = ','.join([str(y),str(x+1)])
    #     up    = ','.join([str(y-1),str(x)])        
    #     left  = ','.join([str(y),str(x-1)])
        

    #     direction_steps = []
    #     if y < len(self.grid) - 1 and down not in visited_tiles and current + 1 >= self.height(y+1,x):
    #         #print("trav down")
    #         direction_steps.append(self.traverse([y+1,x],visited_tiles,steps))
    #     if x < len(self.grid[0]) - 1 and right not in visited_tiles and current + 1 >= self.height(y,x+1):
    #         #print("trav right")
    #         direction_steps.append(self.traverse([y,x+1],visited_tiles,steps))
    #     if y > 0 and up not in visited_tiles and current + 1 >= self.height(y-1,x):
    #         #print("trav up")
    #         direction_steps.append(self.traverse([y-1,x],visited_tiles,steps))        
    #     if x > 0 and left not in visited_tiles and current + 1 >= self.height(y,x-1):
    #         #print("trav left")
    #         direction_steps.append(self.traverse([y,x-1],visited_tiles,steps))


    #     visited_tiles.remove(curr_str)

    #     #If we reached a dead-end, return -1
    #     if len([count for count in direction_steps if count >= 0]) == 0:
    #         return -1

    #     #Otherwise, return the fastest directional step
    #     return min([count for count in direction_steps if count >= 0])

    def height(self,y,x):
        return ord(self.height_grid[y][x])

if __name__ == '__main__':
    Day12().run(INPUT_TYPE)
