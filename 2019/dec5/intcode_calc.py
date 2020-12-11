import sys

from typing import List


class OpcodeNotFound(Exception):
    pass


OPCODE_BYTE_LEN = 2


opcode_parameter_mode = {
    1: {'operation': 'ADD', 'nargs': 3},
    2: {'operation': 'MULTIPLY', 'nargs': 3},
    3: {'operation': 'INPUT', 'nargs': 1},
    4: {'operation': 'OUTPUT', 'nargs': 1},
    5: {'operation': 'JUMP_IF_TRUE', 'nargs': 2},
    6: {'operation': 'JUMP_IF_FALSE', 'nargs': 2},
    7: {'operation': 'LESS_THAN', 'nargs': 3},
    8: {'operation': 'EQUALS', 'nargs': 3},
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
            self._process_instruction(self.instruction_pointer)

    def _process_instruction(self, index: int) -> None:
        opcode = self.opcodes[index]
    
        try:
            op_lookup = opcode_no_parameter_mode[opcode]
        except KeyError:
            try:
                opcode_str = str(opcode)
                matching_op = opcode_str[-2:]
                op_lookup = opcode_parameter_mode[int(opcode_str[-1])]
            except KeyError:
                raise OpcodeNotFound

        # Process no parameter mode instructions
        operation = op_lookup['operation']
        opcode_str = str(opcode).zfill(OPCODE_BYTE_LEN + op_lookup['nargs'])
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
        elif operation == 'JUMP_IF_TRUE':
            self._jump_if_true_opcode(index, modes)
        elif operation == 'JUMP_IF_FALSE':
            self._jump_if_false_opcode(index, modes)
        elif operation == 'LESS_THAN':
            self._less_than_opcode(index, modes)
            self.instruction_pointer += 4
        elif operation == 'EQUALS':
            self._equals_opcode(index, modes)
            self.instruction_pointer += 4

    def _less_than_opcode(self, index: int, modes: List[str]) -> None:
        """
        if the first parameter is less than the second parameter, it
        stores 1 in the position given by the third parameter. Otherwise,
        it stores 0.
        """
        value_1 = self._read(index + 1, modes[0])
        value_2 = self._read(index + 2, modes[1])

        if value_1 < value_2:
            result = 1
        else:
            result = 0

        self._write(index + 3, modes[2], result)

    def _equals_opcode(self, index: int, modes: List[str]) -> None:
        """
        if the first parameter is equal to the second parameter, it
        stores 1 in the position given by the third parameter. Otherwise,
        it stores 0.
        """
        value_1 = self._read(index + 1, modes[0])
        value_2 = self._read(index + 2, modes[1])

        if value_1 == value_2:
            result = 1
        else:
            result = 0

        self._write(index + 3, modes[2], result)

    def _jump_if_true_opcode(self, index: int, modes: List[str]) -> None:
        """
        if the first parameter is non-zero, it sets the instruction pointer
        to the value from the second parameter. Otherwise, it does nothing.
        """
        value_1 = self._read(index + 1, modes[0])
        value_2 = self._read(index + 2, modes[1])
        if value_1 != 0:
            self.instruction_pointer = value_2
        else:
            self.instruction_pointer += 3

    def _jump_if_false_opcode(self, index: int, modes: List[str]) -> None:
        """
        if the first parameter is zero, it sets the instruction pointer
        to the value from the second parameter. Otherwise, it does nothing.
        """
        value_1 = self._read(index + 1, modes[0])
        value_2 = self._read(index + 2, modes[1])
        if value_1 == 0:
            self.instruction_pointer = value_2
        else:
            self.instruction_pointer += 3

    def _write(self, index: int, mode: str, value: int) -> None:
        if mode == 'POSITION':
            position = self.opcodes[index]
            self.opcodes[position] = value
        elif mode == 'IMMEDIATE':
            self.opcodes[index] = value

    def _read(self, index: int, mode: str) -> int:
        if mode == 'POSITION':
            position = self.opcodes[index]
            value = self.opcodes[position]
        elif mode == 'IMMEDIATE':
            value = self.opcodes[index]
        return value

    def _input(self, index: int, modes: List[str]) -> None:
        input_value = int(input("Program needs input (single integer plz): "))
        self._write(index + 1, modes[0], input_value)

    def _output(self, index: int, modes: List[str]) -> None:
        value = self._read(index + 1, modes[0])
        print("Program output: ", value)

    def _arithmetic_opcode(self, index: int, operation: str, modes: List[str]) -> None:
        value_1 = self._read(index + 1, modes[0])
        value_2 = self._read(index + 2, modes[1])

        if operation == 'ADD':
            result = value_1 + value_2
        elif operation == 'MULTIPLY':
            result = value_1 * value_2

        self._write(index + 3, modes[2], result)


if __name__=="__main__":
    with open('input.txt', 'r') as f:
        opcodes = f.read().split(',')

    opcodes = [int(x) for x in opcodes]

    # test case is below
    #opcodes = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99] # test case

    computer = Computer(opcodes)
    computer.process()
