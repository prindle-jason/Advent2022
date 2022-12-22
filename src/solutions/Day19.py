# https://adventofcode.com/2022/day/19
from adventutil.DataImport import InputType
from adventutil.Day import Day
from adventutil.IntHelper import strings_to_ints
from adventutil.ListHelper import zip_sum

from Day19x import RobotChoice, Blueprint, Strategy, BruteForceStrategy

YEAR, DAY = 2022, 19

EXPECTED_A = 1266
EXPECTED_B = 5800
INPUT_TYPE = InputType.LIVE_DATA

class Day19(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        MINUTES = 24
        total = 0
        for bp in [Blueprint(line) for line in strings_to_ints(self.lines)]:
            self.attempts = {}
            for time in range(MINUTES, 0, -1):
                self.attempts[time] = set()
            self.attempts[MINUTES].add((1,0,0,0,0,0,0,0))

            strat = BruteForceStrategy(bp)
            for time in range(MINUTES, 1, -1):
                print(f"Simulating minute {time}.  Considering {len(self.attempts[time])} options.")
                self.prune(time)
                print(f"After pruning there are {len(self.attempts[time])} remaining...")
                self.simulate(strat, time)

            best = 0
            for attempt in self.attempts[1]:
                best = max(best,attempt[3]+attempt[7])      
            total += bp.id * best
        return total

    def partB(self):
        MINUTES = 32

        blueprints = [Blueprint(line) for line in strings_to_ints(self.lines)][:3]

        total = 1
        for bp in blueprints:
            self.attempts = {}
            for time in range(MINUTES, 0, -1):
                self.attempts[time] = set()
            self.attempts[MINUTES].add((1,0,0,0,0,0,0,0))

            strat = BruteForceStrategy(bp)
            for time in range(MINUTES, 1, -1):
                print(f"Simulating minute {time}.  Considering {len(self.attempts[time])} options.")
                self.prune(time)
                print(f"After pruning there are {len(self.attempts[time])} remaining...")
                self.simulate(strat, time)

            best = 0
            for attempt in self.attempts[1]:
                best = max(best,attempt[3]+attempt[7])      
            total *= best

        return total
            
    def simulate(self, strat: Strategy, time):
        for attempt in self.attempts[time]:
            robots, resources = list(attempt[:4]), list(attempt[4:])

            #Use strategy to determine which robots to consider next...
            choices = strat.execute(time, robots, resources)
            
            #Collect resources
            resources = zip_sum(robots, resources)

            for choice in choices:
                if choice is not RobotChoice.NONE:
                    #Buy robot
                    price = strat.bp.get_robot_cost(choice)
                    resources = zip_sum(resources, price)
                    robots[choice.value] += 1

                new_attempt = tuple(robots + resources)

                if new_attempt not in self.attempts[time-1]:            
                    self.attempts[time-1].add(new_attempt)
                
                if choice is not RobotChoice.NONE:
                    #"Sell" robot
                    price = [-i for i in price]
                    resources = zip_sum(resources, price)
                    robots[choice.value] -= 1    

    def prune(self, time):
        '''Remove any attempt that is inherently worse (all values less than or equal to next attempt)
           Also removes any attempt where the geode robot count is 2+ less than the max attempt,
              this is a hacky prune and I'm probably just lucky that it worked.'''
 
        attempt_list = sorted(list(self.attempts[time]))
        max_geo = max([g[3] for g in attempt_list])
        attempt_list = [a for a in attempt_list if a[3] + 1 >= max_geo]


        self.attempts[time] = set()
        for a, b in zip(attempt_list, attempt_list[1:]):
            if self.prune_filter(a,b):
                self.attempts[time].add(a)
        self.attempts[time].add(attempt_list[-1])

    def prune_filter(self, a, b):
        for ax, bx in zip(a, b):
            if ax > bx:
                return True
        return False

if __name__ == '__main__':
    Day19().run(INPUT_TYPE)
