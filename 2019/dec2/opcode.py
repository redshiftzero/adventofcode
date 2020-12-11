import sys

from typing import List


class OpcodeNotFound(Exception):
    pass


opcode_dict = {
    1: 'ADD',
    2: 'MULTIPLY',
    99: 'STOP',
}


class Computer():
    def __init__(self, opcodes: List[int]):
        self.opcodes = opcodes
        self.instruction_pointer = 0
        self.keep_running = True

    def process(self) -> None:
        while self.keep_running:
            self._process_opcode(self.instruction_pointer)
            self.instruction_pointer += 4

    def _arithmetic_opcode(self, index: int, operation: str) -> None:
        position_1 = self.opcodes[index + 1]
        position_2 = self.opcodes[index + 2]
        position_3 = self.opcodes[index + 3]
    
        if operation == 'ADD':
            result = self.opcodes[position_1] + self.opcodes[position_2]
        elif operation == 'MULTIPLY':
            result = self.opcodes[position_1] * self.opcodes[position_2]

        self.opcodes[position_3] = result

    def _process_opcode(self, index: int) -> None:
        opcode = self.opcodes[index]
        try:
            operation = opcode_dict[opcode]
            if operation == 'ADD' or operation == 'MULTIPLY':
                self._arithmetic_opcode(index, operation)
            elif operation == 'STOP':
                self.keep_running = False
        except KeyError:
            raise OpcodeNotFound


if __name__=="__main__":
    with open('input.txt', 'r') as f:
        opcodes = f.read().split(',')

    opcodes = [int(x) for x in opcodes]

    #opcodes = [1,9,10,3,2,3,11,0,99,30,40,50]  # test case
    target_output = 19690720

    # O(N*M) solution
    for verb in range(1, 100):
        for noun in range(1, 100):
            test_opcodes = opcodes.copy()
            test_opcodes[1] = noun
            test_opcodes[2] = verb
            computer = Computer(test_opcodes)
            computer.process()
            if computer.opcodes[0] == target_output:
                print(100 * noun + verb)
