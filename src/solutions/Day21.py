# https://adventofcode.com/2022/day/21
from functools import cmp_to_key
from adventutil.DataImport import InputType
from adventutil.Day import Day

YEAR, DAY = 2022, 21

EXPECTED_A = 38914458159166
EXPECTED_B = 3665520865940
INPUT_TYPE = InputType.LIVE_DATA

class Day21(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        solved_dict, unsolved_list = dict(), list()
        for line in self.lines:
            next = line.replace(':','').split()

            match next:
                case _, _:
                    solved_dict[next[0]] = next[1]
                case _, _, _, _:
                    unsolved_list.append(next)

        while unsolved_list:
            copy = unsolved_list.copy()
            for next in copy[::-1]:
                if next[1] in solved_dict and next[3] in solved_dict:
                    key, first, operator, second = next
                    first, second = solved_dict[first], solved_dict[second]
                    evaluate = ''.join([first,operator,second])
                    solved_dict[key] = str(int(eval(evaluate)))
                    unsolved_list.remove(next)
        
        return int(solved_dict['root'])

    def partB(self):
        #root = None
        solved_dict, unsolved_list = dict(), list()
        for line in self.lines:
            next = line.replace(':','').split()

            match next:
                case 'humn', _:
                    continue
                case _, _:
                    solved_dict[next[0]] = next[1]
                #case 'root', _, _, _:
                #    root = next
                case _, _, _, _:
                    unsolved_list.append(next)

        finished = False
        while not finished:#unsolved_list:
            finished = True
            unsolved_copy = unsolved_list.copy()
            for next in unsolved_copy[::-1]:
                if next[1] in solved_dict and next[3] in solved_dict:
                    finished = False
                    key, first, operator, second = next 
                    evaluation = ''.join([solved_dict[first],operator,solved_dict[second]])
                    solved_dict[key] = str(int(eval(evaluation)))
                    unsolved_list.remove(next)

        # Lots of opportunities to refactor here...
        next = 'root'
        while next != 'humn':
            for unsolved in unsolved_list:
                if next == unsolved[0]:
                    if next != 'root':
                        unsolved[0] = int(solved_dict[next])

                    if unsolved[1] in solved_dict:
                        unsolved[1] = int(solved_dict[unsolved[1]])
                    else:
                        unsolved[3] = int(solved_dict[unsolved[3]])
                    
                    match unsolved:
                        case 'root', str(), _, int():
                            result = unsolved[3]
                            next = unsolved[1]
                        case 'root', int(), _, str():
                            result = unsolved[1]
                            next = unsolved[3]
                            

                        case int(), str(), '+', int():
                            result = unsolved[0] - unsolved[3]
                            next = unsolved[1]
                        case int(), int(), '+', str():
                            result = unsolved[0] - unsolved[1]
                            next = unsolved[3]

                        case int(), str(), '-', int():
                            result = unsolved[0] + unsolved[3]
                            next = unsolved[1]
                        case int(), int(), '-', str():
                            result = unsolved[1] - unsolved[0]
                            next = unsolved[3]

                        case int(), str(), '*', int():
                            result = unsolved[0] / unsolved[3]
                            next = unsolved[1]
                        case int(), int(), '*', str():
                            result = unsolved[0] / unsolved[1]
                            next = unsolved[3]
                        
                        case int(), str(), '/', int():
                            result = unsolved[0] * unsolved[3]
                            next = unsolved[1]
                        case int(), int(), '/', str():
                            result = unsolved[1] / unsolved[0]
                            next = unsolved[3]

                    solved_dict[next] = result

        return int(solved_dict[next])     

if __name__ == '__main__':
    Day21().run(INPUT_TYPE)
