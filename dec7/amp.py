import itertools
import sys

from typing import List, Optional


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
    def __init__(self, opcodes: List[int], inputs: List[int]):
        self.opcodes = opcodes
        self.instruction_pointer = 0
        self.keep_running = True
        self.inputs = inputs
        self.input_generator = itertools.cycle(self.inputs)
        self.outputs = []

    def process(self) -> Optional[List]:
        while self.keep_running:
            self._process_instruction(self.instruction_pointer)
        
        return self.outputs

    def _process_instruction(self, index: int) -> Optional[List]:
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
        input_value = next(self.input_generator)
        self._write(index + 1, modes[0], input_value)

    def _output(self, index: int, modes: List[str]) -> None:
        value = self._read(index + 1, modes[0])
        self.outputs.append(value)

    def _arithmetic_opcode(self, index: int, operation: str, modes: List[str]) -> None:
        value_1 = self._read(index + 1, modes[0])
        value_2 = self._read(index + 2, modes[1])

        if operation == 'ADD':
            result = value_1 + value_2
        elif operation == 'MULTIPLY':
            result = value_1 * value_2

        self._write(index + 3, modes[2], result)


class Amplifier():
    def __init__(self, input_signal: Optional[int] = None):
        if input_signal:
            self.input_signal = input_signal
        self.phase_signal = None  # int
        self.next = None

    def compute(self, program: List[int], program_inputs: List[int]) -> int:
        computer = Computer(program, program_inputs)
        output_signal = computer.process()
        if len(output_signal) != 1:
            raise Exception('incorrect number of outputs')

        return output_signal[0]


class AmplificationCircuit():
    def __init__(self, program: List[int]):
        self.program = program
        self.head = None

    def compute_output_signal(self, phase_settings: List[int]) -> int:
        temp = self.head
        input_signals = [0]  # we only know one at the beginning
        counter = 0
        while temp:
            temp.input_signal = input_signals[-1]
            program_inputs = [phase_settings[counter], temp.input_signal]
            output_signal = temp.compute(self.program, program_inputs)
            input_signals.append(output_signal)
            temp = temp.next
            counter += 1

        return output_signal


if __name__=="__main__":
    with open('input.txt', 'r') as f:
        opcodes = f.read().split(',')

    opcodes = [int(x) for x in opcodes]

    # test cases
    #opcodes = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    #opcodes = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    #opcodes = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

    max_thruster_signal = 0
    best_phase_order = []
    for phase_order in list(itertools.permutations([0, 1, 2, 3, 4])):
        amp = AmplificationCircuit(opcodes)
        amp_A = Amplifier()
        amp.head = amp_A

        amp_B = Amplifier()
        amp_C = Amplifier()
        amp_D = Amplifier()
        amp_E = Amplifier()

        amp_A.next = amp_B
        amp_B.next = amp_C
        amp_C.next = amp_D
        amp_D.next = amp_E

        thruster_signal = amp.compute_output_signal(list(phase_order))

        if thruster_signal > max_thruster_signal:
            max_thruster_signal = thruster_signal
            best_phase_order = phase_order
        
    print(max_thruster_signal)
    print(best_phase_order)




