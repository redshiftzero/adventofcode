import heapq

from typing import Dict, List, Optional


class Orbit():
    def __init__(self, name: str):
        self.name = name
        self.children = []  # List[Orbit]
        self.parents = []  # List[Orbit]

    def __repr__(self) -> str:
        return 'Orbit("{}")'.format(self.name)

    def __lt__(self, other) -> str:
        return other

    def __str__(self) -> str:
        if self.children:
            return '{}){}'.format(self.name, self.children[0].name)
        else:
            return 'Leaf: {}'.format(self.name)

    def add_child(self, child) -> None:
        self.children.append(child)

    def add_parent(self, parent) -> None:
        self.parents.append(parent)


class Universe():
    def __init__(self):
        self.orbits = {}  # type: Dict[Orbit]
        com = Orbit('COM')
        self.root = com
        self.add_orbit(com)

    def __getitem__(self, name: str):
        return self.orbits[name]

    def add_orbit(self, orbit: Orbit) -> None:
        self.orbits[orbit.name] = orbit

    def get_direct_parent(self, child: Orbit) -> Orbit:
        for orbit in list(self.orbits.values()):
            if child in orbit.children:
                return orbit

    def set_parents(self) -> List[Orbit]:
        for x in list(self.orbits.values()):
            for y in list(self.orbits.values()):
                if x in y.children:
                    x.add_parent(y)

    def count_orbits(self) -> int:
        # First exclude the root node (which orbits nothing)
        nodes_to_count = self.orbits.copy()
        num_orbits = 0
        del nodes_to_count['COM']

        for orbit in list(nodes_to_count.values()):
            # We know each node will have at least one parent, since we excluded the root node.
            orbits_this_node = 1
            parent = self.get_direct_parent(orbit)
            while parent != self.root:
                orbit = parent
                orbits_this_node += 1
                parent = self.get_direct_parent(orbit)

            num_orbits += orbits_this_node

        return num_orbits

    def shortest_path(self, start: Orbit, target: Orbit) -> int:
        visited = set()
        q = [[start]]

        nodes_to_traverse = self.orbits.copy()
        del nodes_to_traverse[start.name]

        paths = []
        while q:
            path = q.pop(0)
            node = path[-1]

            if node == target:
                paths.append(path)
            elif node not in visited:
                for neighbor in node.children + node.parents:
                    new_path = list(path)
                    new_path.append(neighbor)
                    q.append(new_path)

                visited.add(node)
            print('visited: {}'.format(node))

        # minus 2 for the start and end nodes
        # minus 1 for the fact we want the "orbital transfers"
        distances = [len(x) - 2 - 1 for x in paths]
        print(paths)
        return min(distances)


if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        input_ = f.readlines()

    #input_ = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F',
    #          'B)G', 'G)H', 'D)I', 'E)J', 'J)K',
    #          'K)L', 'K)YOU', 'I)SAN']

    universe = Universe()
    for line in input_:
        parent_name, child_name = line.strip('\n').split(')')
        try:
            child_orbit = universe[child_name]
        except KeyError:
            child_orbit = Orbit(child_name)
            universe.add_orbit(child_orbit)

        try:
            parent_orbit = universe[parent_name]
        except KeyError:
            parent_orbit = Orbit(parent_name)
            universe.add_orbit(parent_orbit)
        
        parent_orbit.add_child(child_orbit)

    universe.set_parents()
    start = universe['YOU']
    target = universe['SAN']
    print(universe.shortest_path(start, target))