# https://adventofcode.com/2022/day/16
from dataclasses import dataclass
from itertools import product
from adventutil.DataImport import InputType
from adventutil.Day import Day
from adventutil.IntHelper import string_to_ints

from Day16x import Graph, Node, Worker

YEAR, DAY = 2022, 16

EXPECTED_A = 1673
EXPECTED_B = 2343
INPUT_TYPE = InputType.LIVE_DATA

class Day16(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)
        self.best_b = 0

    def partA(self):
        self.graph = Graph(self.lines)
        START_TIME = 30
        return self.traverse_a('AA', [], START_TIME, 0)

    def partB(self):
        self.graph = Graph(self.lines)
        START_TIME = 26
        return self.traverse_b(Worker('AA', START_TIME), Worker('AA', START_TIME), [], 0)

    def traverse_a(self, current_node_id, active_node_ids, time_left, flow):
        candidate_nodes = self.find_candidate_nodes(current_node_id, active_node_ids, time_left, flow)

        if not candidate_nodes:
            return flow
        
        best_result = flow
        for (n,f,t) in candidate_nodes:
            active_node_ids.append(n.id)
            best_result = max(best_result, self.traverse_a(n.id, active_node_ids, time_left-t, flow+f))
            active_node_ids.remove(n.id)
        return best_result

    def traverse_b(self, w1: Worker, w2: Worker, active_node_ids, flow):
        time_left = max(w1.next_open, w2.next_open)

        w1_candidates, w2_candidates = None, None
        if w1.next_open == time_left:
            w1_candidates = self.find_candidate_nodes(w1.target_id, active_node_ids, time_left, flow)                
        if w2.next_open == time_left:
            w2_candidates = self.find_candidate_nodes(w2.target_id, active_node_ids, time_left, flow)

        if not w1_candidates and not w2_candidates:
            return flow

        trials = []
        if w1_candidates and w2_candidates:
            for ((n1, f1, t1),(n2, f2, t2)) in product(w1_candidates, w2_candidates):
                if n1 == n2:
                    continue
                trials.append(([n1.id,n2.id], Worker(n1.id, time_left-t1), Worker(n2.id, time_left-t2), f1 + f2))
        elif w1_candidates:
            for (n, f, t) in w1_candidates:
                trials.append(([n.id], Worker(n.id, time_left-t), w2, f))
        elif w2_candidates:
            for (n, f, t) in w2_candidates:
                trials.append(([n.id], w1, Worker(n.id, time_left-t), f))

        best_result = flow
        for (next_actives, new_w1, new_w2, new_flow) in trials:
            active_node_ids.extend(next_actives)
            
            best_result = max(best_result,self.traverse_b(new_w1, new_w2, active_node_ids, flow+new_flow))
            
            [active_node_ids.remove(next) for next in next_actives]

        if best_result > self.best_b:
            self.best_b = best_result

        return best_result

    def find_candidate_nodes(self, current_node_id, active_node_ids, time_left, flow_so_far):
        viable_options = []
        candidate_nodes = [(self.graph.get_node(id),cost) for (id,cost) in self.graph.paths[current_node_id].items() if id not in active_node_ids]
        
        #Attempt to prune branches that can't beat best found so far, even if we could go to every valve and open at the same time    
        theoretical_best = flow_so_far + sum([node.rate*(time_left-cost) for (node,cost) in candidate_nodes])
        if theoretical_best < self.best_b:
            return None
        
        for (node, cost) in candidate_nodes:
            flow_score = node.rate * (time_left - cost)
            if flow_score > 0:
                viable_options.append((node, flow_score, cost))

        return sorted(viable_options, key=lambda x:x[1], reverse=True) if len(viable_options) > 0 else None

if __name__ == '__main__':
    Day16().run(INPUT_TYPE)
