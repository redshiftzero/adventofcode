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

    def process(self) -> None:
        while True:
            #print('processing: {}'.format(self.instruction_pointer))
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
            #print(operation)
            if operation == 'ADD' or operation == 'MULTIPLY':
                self._arithmetic_opcode(index, operation)
            elif operation == 'STOP':
                print(self.opcodes)
                sys.exit(0)
        except KeyError:
            raise OpcodeNotFound


if __name__=="__main__":
    with open('input.txt', 'r') as f:
        opcodes = f.read().split(',')

    opcodes = [int(x) for x in opcodes]

    opcodes[1] = 12
    opcodes[2] = 2
    #opcodes = [1,9,10,3,2,3,11,0,99,30,40,50]  # test case
    computer = Computer(opcodes)
    computer.process()
