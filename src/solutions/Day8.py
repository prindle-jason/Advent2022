# https://adventofcode.com/2022/day/8
from adventutil.DataImport import InputType
from adventutil.Day import Day
from adventutil.GridHelper import get_numeric_grid

YEAR, DAY = 2022, 8

EXPECTED_A = 1698
EXPECTED_B = 672280
INPUT_TYPE = InputType.LIVE_DATA

class Day8(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        grid = get_numeric_grid(self.lines)
        grid_width, grid_height = len(grid[0]), len(grid)

        count = 2 * (grid_width+grid_height-2)  # Automatically count exterior trees
        for y in range(1,grid_height-1):
            for x in range(1,grid_width-1):
                tree = grid[y][x]

                # Find highest tree in each direction
                top = max([row[x] for row in grid[:y]])
                bot = max([row[x] for row in grid[y+1:]])
                left = max(grid[y][:x])
                right = max(grid[y][x+1:])

                if tree > min(top,bot,left,right):
                    count += 1

        return count

    def partB(self):
        grid = get_numeric_grid(self.lines)
        grid_width, grid_height = len(grid[0]), len(grid)

        max_score = 0
        for row in range(grid_height):
            for column in range(grid_width):
                tree = grid[row][column]
                
                top_score, bot_score, left_score, right_score = 0,0,0,0

                for t in range(row-1, -1, -1):
                    top_score += 1
                    if(grid[t][column] >= tree):
                        break

                for b in range(row+1, grid_height):
                    bot_score += 1
                    if grid[b][column] >= tree:
                        break
                        
                for l in range(column-1, -1, -1):
                    left_score += 1 
                    if grid[row][l] >= tree:
                        break
       
                for r in range(column+1, grid_width):
                    right_score += 1 
                    if grid[row][r] >= tree:
                        break
                         
                tree_score = top_score * bot_score * left_score * right_score  
                max_score = max(max_score, tree_score)

        return max_score

if __name__ == '__main__':
    Day8().run(INPUT_TYPE)
