import math

from typing import List


def compute_fuel(mass: int) -> int:
    return math.floor(mass / 3) - 2


class Launch():
    def __init__(self, module_masses: List[int]):
        self.modules = []
        for mass in module_masses:
            module = Module(mass)
            self.modules.append(module)

    def get_fuel(self) -> int:
        total_fuel = 0
        for module in self.modules:
            total_fuel += module.get_fuel()
        return total_fuel


class Module():
    def __init__(self, mass: int):
        self.mass = mass
    
    def get_fuel(self) -> int:
        fuel_to_compute = True
        total_fuel = 0
        mass = self.mass

        while fuel_to_compute:
            fuel_required = compute_fuel(mass)

            if fuel_required <= 0:
                fuel_to_compute = False
            else:
                total_fuel += fuel_required
                mass = fuel_required  # For next iteration

        return total_fuel


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    #modules = [12, 14, 1969, 100756]  # test cases
    modules = [int(x) for x in lines]
    launch = Launch(modules)
    print(launch.get_fuel())
