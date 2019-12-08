import itertools
import sys
from threading import Thread
from queue import Queue

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
    def __init__(self, opcodes: List[int], identifier: str, inputs: Queue, outputs: Queue,
                 phase_signal: int):
        self.opcodes = opcodes
        self.identifier = identifier
        self.instruction_pointer = 0
        self.keep_running = True
        self.inputs: Queue = inputs
        self.outputs: Queue = outputs
        self.phase_signal: Optional[int] = phase_signal

    def process(self) -> Optional[List]:
        while self.keep_running:
            self._process_instruction(self.instruction_pointer)

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
        if self.phase_signal:
            input_value = self.phase_signal
            self.phase_signal = None
        else:
            input_value = self.inputs.get()
        self._write(index + 1, modes[0], input_value)

    def _output(self, index: int, modes: List[str]) -> None:
        value = self._read(index + 1, modes[0])
        self.outputs.put(value)

    def _arithmetic_opcode(self, index: int, operation: str, modes: List[str]) -> None:
        value_1 = self._read(index + 1, modes[0])
        value_2 = self._read(index + 2, modes[1])

        if operation == 'ADD':
            result = value_1 + value_2
        elif operation == 'MULTIPLY':
            result = value_1 * value_2

        self._write(index + 3, modes[2], result)


class Amplifier():
    def __init__(self, identifier: str, phase_signal: Optional[int] = None):
        self.phase_signal = phase_signal
        self.identifier = identifier
        self.next = None

    def compute(self, program: List[int], inputs: Queue, outputs: Queue) -> int:
        self.computer = Computer(program.copy(), self.identifier, inputs, outputs, self.phase_signal)
        self.computer.process()

    def reassign_input_queue(self, inputs: Queue) -> None:
        self.computer.inputs = inputs


class AmplificationCircuit():
    def __init__(self, program: List[int]):
        self.program = program
        self.head = None

    def compute_output_signal(self) -> int:
        temp = self.head
        threads = {}

        out_q = None
        feedback_setup = False
        # We only need to traverse the linked list once to setup the threads, queues, and
        # start them all.
        while temp and not feedback_setup:
            try:
                thread_temp = threads[temp.identifier]['thread']

                # Connect the feedback loop
                if temp.identifier == 'A' and not feedback_setup:
                    out = threads['E']['out_q'].get()
                    threads['A']['in_q'].put(out)
                    threads['A']['in_q'] = threads['E']['out_q']
                    temp.reassign_input_queue(threads['E']['out_q'])
                    feedback_setup = True
            except KeyError:
                # Make the shared queues
                in_q = Queue()

                if out_q:  # Then this is not the first node
                    in_q = out_q
                    last_output = out_q.get()
                    in_q.put(last_output)
                else:  # This is the first node
                    in_q.put(0)

                out_q = Queue()

                # Make the thread to run the intcode computer and set it running
                threads[temp.identifier] = {
                    'obj': temp,
                    'in_q': in_q,
                    'out_q': out_q,
                    'thread': Thread(target = temp.compute, 
                                     args=(self.program, in_q, out_q, ))
                }
                threads[temp.identifier]['thread'].start()
            temp = temp.next

        threads['E']['thread'].join()
        output = threads['E']['out_q'].get()
        return output


if __name__=="__main__":
    with open('input.txt', 'r') as f:
        opcodes = f.read().split(',')

    opcodes = [int(x) for x in opcodes]

    # test cases
    #opcodes = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    #opcodes = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

    max_thruster_signal = 0
    best_phase_order = []
    for phase_order in list(itertools.permutations([9,8,7,6,5])):
        amp = AmplificationCircuit(opcodes)
        amp_A = Amplifier('A', phase_order[0])
        amp.head = amp_A

        # We'll run each amplifier's intcode computer in its own thread,
        # and use queues between the links for inter-thread communication.
        amp_B = Amplifier('B', phase_order[1])
        amp_C = Amplifier('C', phase_order[2])
        amp_D = Amplifier('D', phase_order[3])
        amp_E = Amplifier('E', phase_order[4])

        amp_A.next = amp_B

        amp_B.next = amp_C
        amp_C.next = amp_D
        amp_D.next = amp_E
        # Adds a feedback loop to the linked list
        amp_E.next = amp_A

        thruster_signal = amp.compute_output_signal()

        if thruster_signal > max_thruster_signal:
            max_thruster_signal = thruster_signal
            best_phase_order = phase_order
        
    print(max_thruster_signal)
    print(best_phase_order)



