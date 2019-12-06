import sys

from typing import List


class OpcodeNotFound(Exception):
    pass


# Opcodes that have parameter mode support.
opcode_parameter_mode = {
    1: {'operation': 'ADD', 'nargs': 3},
    2: {'operation': 'MULTIPLY', 'nargs': 3},
    3: {'operation': 'INPUT', 'nargs': 1},
    4: {'operation': 'OUTPUT', 'nargs': 1},
}

opcode_no_parameter_mode = {
    99: {'operation': 'STOP', 'nargs': 0},
}

param_mode_dict = {
    0: 'POSITION',
    1: 'IMMEDIATE',
}


class Computer():
    def __init__(self, opcodes: List[int]):
        self.opcodes = opcodes
        self.instruction_pointer = 0
        self.keep_running = True

    def process(self) -> None:
        while self.keep_running:
            self._process_opcode(self.instruction_pointer)

    def _process_opcode(self, index: int) -> None:
        opcode = self.opcodes[index]
    
        try:
            op_lookup = opcode_no_parameter_mode[opcode]
        except KeyError:
            try:
                opcode_str = str(opcode).zfill(5)
                matching_op = opcode_str[-2:]
                op_lookup = opcode_parameter_mode[int(opcode_str[-1])]
            except KeyError:
                raise OpcodeNotFound

        # Process no parameter mode instructions
        operation = op_lookup['operation']
        if operation == 'STOP':
            self.keep_running = False

        # Process parameter mode instructions
        modes = []
        for arg in reversed(range(op_lookup['nargs'])):
            mode = param_mode_dict[int(opcode_str[arg])]
            modes.append(mode)

        if operation == 'ADD' or operation == 'MULTIPLY':
            self._arithmetic_opcode(index, operation, modes)
            self.instruction_pointer += 4
        elif operation == 'INPUT':
            self._input(index, modes)
            self.instruction_pointer += 2
        elif operation == 'OUTPUT':
            self._output(index, modes)
            self.instruction_pointer += 2

    def _opcode_write(self, index: int, mode: str, value: int) -> None:
        if mode == 'POSITION':
            position = self.opcodes[index]
            self.opcodes[position] = value
        elif mode == 'IMMEDIATE':
            self.opcodes[index] = value

    def _opcode_read(self, index: int, mode: str) -> int:
        if mode == 'POSITION':
            position = self.opcodes[index]
            value = self.opcodes[position]
        elif mode == 'IMMEDIATE':
            value = self.opcodes[index]
        return value

    def _input(self, index: int, modes: List[str]) -> None:
        input_value = int(input("Program needs input (single integer plz): "))
        self._opcode_write(index + 1, modes[0], input_value)

    def _output(self, index: int, modes: List[str]) -> None:
        value = self._opcode_read(index + 1, modes[0])
        print("Program output: ", value)

    def _arithmetic_opcode(self, index: int, operation: str, modes: List[str]) -> None:
        value_1 = self._opcode_read(index + 1, modes[0])
        value_2 = self._opcode_read(index + 2, modes[1])

        if operation == 'ADD':
            result = value_1 + value_2
        elif operation == 'MULTIPLY':
            result = value_1 * value_2

        self._opcode_write(index + 3, modes[2], result)


if __name__=="__main__":
    with open('input.txt', 'r') as f:
        opcodes = f.read().split(',')

    opcodes = [int(x) for x in opcodes]

    # opcodes = [3,0,4,0,99]  # test case

    computer = Computer(opcodes)
    computer.process()
