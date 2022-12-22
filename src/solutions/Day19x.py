from abc import ABC, abstractmethod
from enum import Enum

from adventutil.ListHelper import zip_sum

class RobotChoice(Enum):
    ORE  = 0
    CLY  = 1
    OBS  = 2
    GEO  = 3
    NONE = 4

class Blueprint:
    def __init__(self, lst):
        self.id = lst[0]
        self.costs = []
        self.costs.append([-1*lst[1],0,0,0])
        self.costs.append([-1*lst[2],0,0,0])
        self.costs.append([-1*lst[3],-1*lst[4],0,0])
        self.costs.append([-1*lst[5],0,-1*lst[6],0])

    def get_robot_cost(self, choice):
        return self.costs[choice.value]

    def can_afford_robot(self, choice, resources):
        costs = self.get_robot_cost(choice)
        return min(zip_sum(resources, costs)) >= 0

class Strategy(ABC):
    def __init__(self, bp: 'Blueprint'):
        self.bp: 'Blueprint' = bp
        self.before()

    def before(self):
        pass

    @abstractmethod
    def execute(self,minute,robots,resources) -> list[RobotChoice]:
        ...

class BruteForceStrategy(Strategy):
    '''Tries to buy everything it can afford'''
    def execute(self,minute,robots,resources):
        choices = []
        for choice in RobotChoice:
            if choice is RobotChoice.NONE or self.bp.can_afford_robot(choice, resources):
                choices.append(choice)
        return list(reversed(choices))

class GreedyStrategy(Strategy):
    '''Buys first thing it can afford'''
    def execute(self,minute,robots,resources):
        for choice in RobotChoice:
            if self.bp.can_afford_robot(choice, resources):
                return [choice]
        return [RobotChoice.NONE]

class RampStrategy(Strategy):
    '''Buys enough ore and clay robots to produce 1 obsidian and 1 geode per day'''
    def before(self):
        self.ore_robot_target = -1 * (self.bp.costs[2][0] + self.bp.costs[3][0])
        self.cly_robot_target = -1 * self.bp.costs[2][0]

    def execute(self,minute,robots,resources):

        #Should buy ORE?
        if robots[0] < self.ore_robot_target and self.bp.can_afford_robot(RobotChoice.ORE, resources):
            return [RobotChoice.ORE]

        #Should buy CLY?
        if robots[0] == self.ore_robot_target \
                and robots[1] < self.cly_robot_target \
                and self.bp.can_afford_robot(RobotChoice.CLY, resources):
            return [RobotChoice.CLY]

        #Should buy GEO or OBS?
        if robots[0] == self.ore_robot_target and robots[1] == self.cly_robot_target:
            if self.bp.can_afford_robot(RobotChoice.GEO, resources):
                return [RobotChoice.GEO]
            if self.bp.can_afford_robot(RobotChoice.OBS, resources):
                return [RobotChoice.OBS]

        return [RobotChoice.NONE]



