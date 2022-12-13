# https://adventofcode.com/2022/day/13
from adventutil.DataImport import InputType
from adventutil.Day import Day
from adventutil.ListHelper import list_split

YEAR, DAY = 2022, 13

EXPECTED_A = 5623
EXPECTED_B = 20570
INPUT_TYPE = InputType.LIVE_DATA

class Day13(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        pairings = list_split(self.lines,'')
        count = 0
        for index, pairing in enumerate(pairings):
            pairing[0], pairing[1] = eval(pairing[0]), eval(pairing[1])
            #print(pairing)
            correct_order = self.compare_lists(pairing[0],pairing[1])
            print(f"Result: {correct_order}")
            if correct_order == 1:
                print(index)
                count += index + 1
        
        return count

    def compare_lists(self,first_list,second_list):
        for index, a in enumerate(first_list):
            
            if len(second_list) < index + 1:
                return -1

            b = second_list[index]
            #print(f"Comparing elements {a} and {b}")
            #print(f"Comparing elements {a} {type(a)} and {b} {type(b)}")

            inner_result = 0
            if isinstance(a, int) and isinstance(b, int):
                #print("int, int")
                if a < b:
                    return 1
                elif a > b:
                    return -1
                continue
            if isinstance(a, list) and isinstance(b, list):
                #print("list, list")
                inner_result = self.compare_lists(a,b)
                #if result != 0:
                #    return result
            if isinstance(a, int) and isinstance(b, list):
                #print("int, list")
                inner_result = self.compare_lists([a],b)
            if isinstance(a, list) and isinstance(b, int): 
                #print("list, int")               
                inner_result = self.compare_lists(a,[b])
            
            if inner_result != 0:
                return inner_result

        #Check if second list had more elements remaining
        if len(first_list) < len(second_list):
            return 1
        return 0

    def partB(self):
        distress_a = [[2]]
        distress_b = [[6]]

        packets = [distress_a,distress_b]
        for line in self.lines:
            if line != '':
                packets.append(eval(line))
            
        from functools import cmp_to_key
        packets = sorted(packets, key=cmp_to_key(self.compare_lists))
        packets.reverse()
        
        #print(packets)
        #print(packets.index(distress_a))
        #print(packets.index(distress_b))

        return (packets.index(distress_a) + 1) * (packets.index(distress_b) + 1)

if __name__ == '__main__':
    Day13().run(INPUT_TYPE)
