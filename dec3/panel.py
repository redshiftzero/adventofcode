from typing import List, Union


class Point():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.num_steps = None  # Optional[int]

    def __lt__(self, other):
        if self.num_steps < other.num_steps:
            return True
        return False

    def __eq__(self, other) -> bool:
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __repr__(self) -> str:
        return 'Point({}, {})'.format(self.x, self.y)

    def __hash__(self) -> str:  # need for set operations later
        return hash(self.x + self.y)


STARTING_POINT = Point(0, 0)


class SparseGrid():
    def __init__(self, path: List[str]) -> None:
        self._counter: int = 0
        self.path: str = path
        self.points: List = []
        self._construct_visited_points()

    def __getitem__(self, p: Union[int, Point]):
        # Allow fetching points by position in the path.
        if isinstance(p, int):
            return self.points[p]

        # There can be multiple matches since the path may visit the
        # same point multiple times. Since what we care about is the
        # minimum num_steps point, we return that.
        matches = []
        for point in self.points:
            if p == point:
                matches.append(point)

        if len(matches) != 0:
            return min(matches)

        raise KeyError('{} not found in SparseGrid'.format(p))

    def __repr__(self) -> str:
        return 'SparseGrid({})'.format(self.path)

    def __iter__(self):
        return self
    
    def __next__(self):
        self._counter += 1
        try:
            return self.points[self._counter]
        except IndexError:
            self._counter = 0
            return self.points[self._counter]

    def _add_point(self, direction: str, prev_x: int, prev_y: int) -> Point:
        if direction == 'D':
            point = Point(prev_x, prev_y - 1)
        elif direction == 'U':
            point = Point(prev_x, prev_y + 1)
        elif direction == 'L':
            point = Point(prev_x - 1, prev_y)
        elif direction == 'R':
            point = Point(prev_x + 1, prev_y)

        self.points.append(point)
        return point

    def _construct_visited_points(self):
        prev_point = STARTING_POINT
        total_steps = 0
        for step in self.path:
            direction = step[0]
            num_moves = int(step[1:])

            while num_moves > 0:
                total_steps += 1
                point = self._add_point(direction, prev_point.x, prev_point.y)
                point.num_steps = total_steps
                num_moves -= 1
                prev_point = point


def manhattan_distance(p1: Point, p2: Point) -> int:
    return abs(p2.x - p1.x) + abs(p2.y - p1.y)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        input_ = f.readlines()

    wire_1 = input_[0].split(',')
    wire_2 = input_[1].split(',')
    # test input 1
    #wire_1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'.split(',')
    #wire_2 = 'U62,R66,U55,R34,D71,R55,D58,R83'.split(',')
    # test input 2
    #wire_1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'.split(',')
    #wire_2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.split(',')

    # make a grid, mark points that are visited. Do not mark initial point.
    # matrix would be sparse so instead of a huge matrix let's store sparse grids
    # (yes I could use numpy/scipy but I'm intentionally not because
    # this is a programming exercise.)
    sparse_grid_1 = SparseGrid(wire_1)
    sparse_grid_2 = SparseGrid(wire_2)

    intersecting_points = list(set(sparse_grid_1.points) & set(sparse_grid_2.points))

    dists_to_start = [manhattan_distance(x, STARTING_POINT) for x in intersecting_points]

    combined_steps = [sparse_grid_1[x].num_steps + sparse_grid_2[x].num_steps 
                      for x in intersecting_points]

    print('min manhattan distance: {}'.format(min(dists_to_start)))
    print('fewest combined steps: {}'.format(min(combined_steps)))
