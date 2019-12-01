import math


class Module():
    def __init__(self, mass: int):
        self.mass = mass
    
    def get_fuel(self) -> int:
        fuel_required = math.floor(self.mass / 3) - 2
        return fuel_required


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    # test cases
    # modules = [12, 14, 1969, 100756]
    modules = [int(x) for x in lines]

    total_fuel = 0
    for module in modules:
        mod = Module(module)
        total_fuel += mod.get_fuel()
    print(total_fuel)