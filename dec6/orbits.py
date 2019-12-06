from typing import Dict, List, Optional


class Orbit():
    def __init__(self, name: str):
        self.name = name
        self.children = []  # List[Orbit]

    def __repr__(self) -> str:
        return 'Orbit("{}")'.format(self.name)

    def __str__(self) -> str:
        if self.children:
            return '{}){}'.format(self.name, self.children[0].name)
        else:
            return 'Leaf: {}'.format(self.name)

    def add_child(self, child) -> None:
        self.children.append(child)


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


if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        input_ = f.readlines()

    # test input
    #input_ = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G',
    #          'G)H', 'D)I', 'E)J', 'J)K', 'K)L']

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
    
    print(universe.count_orbits())