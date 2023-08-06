#!/usr/bin/env python3

from argparse import ArgumentParser

class bf:
    def __init__(self, file_path, program=None):
        self.valid_commands = ["+", "-", "<", ">", ".", ",", "[", "]"]
        self.arr = [0]
        self.ci = 0
        self.user_input = []
        self.loop_table = {}
        self.loop_stack = []
        self.program = program
        
        if program is None:
            try:
                with open(file_path, "r") as file:
                    self.program = file.read()
            except:
                print("Could not read file")
                self.program = input("Input the brainfuck code: ")

        self.create_loop_table()

    def create_loop_table(self):
        for ip, cmd in enumerate(self.program):
            if cmd == "[":
                self.loop_stack.append(ip)
            elif cmd == "]":
                loop_begin = self.loop_stack.pop()
                self.loop_table[loop_begin] = ip
                self.loop_table[ip] = loop_begin

    def execute(self):
        ip = 0
        while ip < len(self.program):
            cmd = self.program[ip]

            if cmd in self.valid_commands:
                if cmd == "+":
                    self.arr[self.ci] += 1
                    if self.arr[self.ci] == 256:
                        self.arr[self.ci] = 0
                elif cmd == "-":
                    self.arr[self.ci] -= 1
                    if self.arr[self.ci] == -1:
                        self.arr[self.ci] = 255
                elif cmd == "<":
                    self.ci -= 1
                elif cmd == ">":
                    self.ci += 1
                    if self.ci == len(self.arr):
                        self.arr.append(0)
                elif cmd == ".":
                    print(chr(self.arr[self.ci]), end="")
                elif cmd == ",":
                    if self.user_input == []:
                        self.user_input = list(input() + "\n")
                    self.arr[self.ci] = ord(self.user_input.pop(0))
                elif cmd == "[":
                    if self.arr[self.ci] == 0:
                        ip = self.loop_table[ip]
                elif cmd == "]":
                    if self.arr[self.ci]:
                        ip = self.loop_table[ip]

            ip += 1


def main():

    parser = ArgumentParser(
        prog="Brainfuck Interpreter",
        description="The program executes brainfuck code!",
    )
    parser.add_argument(
        "file",
        help="Path to a file that contains brainfuck code",
    )
    args = parser.parse_args()

    interpreter = bf(args.file)
    interpreter.execute()


if __name__ == "__main__":
    main()
