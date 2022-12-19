from dataclasses import dataclass

@dataclass
class Worker:
    target_id: str
    next_open: int

class Graph:
    def __init__(self, lines):
        self.nodes: list[Node] = self._load_nodes(lines)
        self.paths = {}
        self._load_paths()

    def get_node(self,id):
        for node in self.nodes:
            if node.id == id:
                return node
        return None

    def _load_nodes(self, lines):
        nodes = list[Node]()        
        for line in lines:
            input = line.replace(',','').split()
            id, rate, tunnels = input[1], int(input[4][5:-1]), input[9:]
            nodes.append(Node(id, rate, tunnels))

        for node in nodes:
            node.load_tunnels(nodes)  
        return nodes

    def _load_paths(self):
        tracked_nodes = [n for n in self.nodes if n.id == 'AA' or n.rate > 0]
        for node in tracked_nodes:
            self.paths[node.id] = dict()

        #For each node, search for shortest path to every other node... gl
        for index, start in enumerate(tracked_nodes):
            #print(f"Finding shortest routes for node #{index+1}")
            for end in tracked_nodes[index+1:]:
                #Add one to include opening the valve
                shortest = self._load_path(start, end, 0, [start.id]) + 1
                self.paths[start.id][end.id] = shortest
                self.paths[end.id][start.id] = shortest    
    
    def _load_path(self, current, target, steps, visited_ids):
        if target in current.tunnels:
            return steps + 1

        #Check if we already found a route from current to target
        #Subtract one so we don't count "opening valve" several times
        if current.id in self.paths and target.id in self.paths[current.id]:
            return steps + self.paths[current.id][target.id] - 1

        #otherwise
        tunnel_routes = []
        for tunnel in current.tunnels:
            #if we've already visited, skip tunnel
            if tunnel.id in visited_ids:
                continue

            visited_ids.append(tunnel.id)
            total_route = self._load_path(tunnel, target, steps+1, visited_ids)
            
            if total_route > 0:
                tunnel_routes.append(total_route)
            visited_ids.remove(tunnel.id)

        if tunnel_routes and min(tunnel_routes) > 0:
            return min(tunnel_routes)
        return -99999999

class Node:
    def __init__(self, id, rate, tunnel_ids):
        self.id = id
        self.rate = rate
        self.tunnel_ids = tunnel_ids
        self.tunnels = None

    def load_tunnels(self, all_nodes):
        self.tunnels = []
            
        for node in all_nodes:
            if node.id == self.id:
                continue
            if node.id in self.tunnel_ids:
                self.tunnels.append(node)

    def __repr__(self):
        return f"Node {self.id}, rate {self.rate}, tunnels {self.tunnel_ids}"
