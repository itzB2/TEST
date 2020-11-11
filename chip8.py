import os
from random import random

def get_bit(value, index):
    return (value >> index) & 0x01

class CHIP8:
    def __init__(self):
        self.registers = [0]*16
        self.memory = [0]*4096
        self.index = 0
        self.pc = 0
        self.stack = [0]*16
        self.sp = 0
        self.delayTimer = 0
        self.soundTimer = 0
        self.KeyPad = [0]*16
        self.video = [[ 0 for i in range(64) ] for j in range(32)]
        self.opcode = 0

        self.HEIGHT = 32
        self.WIDTH = 64
        self.START_ADDRESS = 0x200
        self.FONTSET_START_ADDRESS = 0x50

        self.pc = self.START_ADDRESS

        self.FontSet = [    
            0x00F0, 0x90, 0x90, 0x90, 0x00F0,
            0x20, 0x60, 0x20, 0x20, 0x70,
            0x00F0, 0x10, 0x00F0, 0x80, 0x00F0,
            0x00F0, 0x10, 0x00F0, 0x10, 0x00F0,
            0x90, 0x90, 0x00F0, 0x10, 0x10,
            0x00F0, 0x80, 0x00F0, 0x10, 0x00F0,
            0x00F0, 0x80, 0x00F0, 0x90, 0x00F0,
            0x00F0, 0x10, 0x20, 0x40, 0x40,
            0x00F0, 0x90, 0x00F0, 0x90, 0x00F0,
            0x00F0, 0x90, 0x00F0, 0x10, 0x00F0,
            0x00F0, 0x90, 0x00F0, 0x90, 0x90,
            0xE0, 0x90, 0xE0, 0x90, 0xE0,
            0x00F0, 0x80, 0x80, 0x80, 0x00F0,
            0xE0, 0x90, 0x90, 0x90, 0xE0,
            0x00F0, 0x80, 0x00F0, 0x80, 0x00F0,
            0x00F0, 0x80, 0x00F0, 0x80, 0x80 
                        ]

        for i in range(0, 80):
            self.memory[self.FONTSET_START_ADDRESS+i] = self.FontSet[i]

    def loadROM(self, path):
        f = open(path, "rb").read()
        size = os.stat(path).st_size
        fileBuffer = open(path, "rb").read()
        for i in range(0, size):
            self.memory[self.START_ADDRESS+i] = fileBuffer[i]

    def setWhite(self, privelages=False):
        if privelages:
            self.video = [[ 1 for i in range(32) ] for j in range(64)]    

    def OP_00E0(self):
        self.video = [[ 0 for i in range(32) ] for j in range(64)]

    def OP_00EE(self):
        self.sp-=1

        self.pc = self.stack[self.sp]

    def OP_1NNN(self):
        address = self.opcode & 0x0FFF
        self.pc = address

    def OP_2NNN(self):
        address = self.opcode & 0x0FFF
        self.stack.pop()
        self.stack.append(self.pc)
        self.sp+=2
        self.pc = address

    def OP_3XKK(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        byte = self.opcode & 0x00FF

        if self.registers[Vx] == byte:
            self.pc += 2;

    def OP_4XKK(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        byte = self.opcode & 0x00FF

        if self.registers[Vx] != byte:
            self.pc += 2;

    def OP_5XY0(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        Vy = (self.memory[self.pc+1] & 0x00F0) >> 4

        if self.registers[Vx] == self.registers[Vy]:
            self.pc += 2

    def OP_6XKK(self):
        Vx = (self.opcode & 0x0FFF) >> 8
        byte = self.opcode & 0x00FF

        self.registers[Vx] = byte

    def OP_7XKK(self):
        Vx = (self.opcode & 0x0FFF) >> 8
        byte = self.opcode & 0x00FF
        b = self.registers[Vx]
        b += byte
        self.registers[Vx] = b

    def OP_8XY0(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        Vy = (self.memory[self.pc+1] & 0x00F0) >> 4

        self.registers[Vx] = self.registers[Vy]

    def OP_8XY1(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        Vy = (self.opcode & 0x00F0) >> 4

        self.registers[Vx] |= self.registers[Vy]

    def OP_8XY2(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        Vy = (self.opcode & 0x00F0) >> 4

        self.registers[Vx] &= self.registers[Vy]

    def OP_8XY3(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        Vy = (self.opcode & 0x00F0) >> 4

        self.registers[Vx] ^= self.registers[Vy]

    def OP_8XY4(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        Vy = (self.opcode & 0x00F0) >> 4

        Vsum = self.registers[Vx] + self.registers[Vy]

        if Vsum > 255:
            self.registers[0xF] = 1
        else:
            self.registers[0xF] = 0

        self.registers = Vsum & 0xFF

    def OP_8XY5(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        Vy = (self.opcode & 0x00F0) >> 4

        if self.registers[Vx] > self.registers[Vy]:
            self.registers[0xF] = 1
        else:
            self.registers[0xF] = 0

        self.registers[Vx] -= self.registers[Vy]
    
    def OP_8XY6(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8

        self.registers[0xF] = (self.registers[Vx] & 0x1)
        self.registers[Vx] >>= 1

    def OP_8XY7(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        Vy = (self.opcode & 0x00F0) >> 4

        if self.registers[Vy] > self.registers[Vx]:
            self.registers[0xF] = 1
        else:
            self.registers[0xF] = 0

        self.registers[Vx] = self.registers[Vy] - self.registers[Vx]

    def OP_8XYE(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        self.registers[0xF] = (self.registers[Vx] & 0x80) >> 7
        self.registers[Vx] <<= 1

    def OP_9XY0(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        Vy = (self.memory[self.pc+1] & 0x00F0) >> 4

        if self.registers[Vx] != self.registers[Vy]:
            self.pc += 2

    def OP_ANNN(self):
        address = self.opcode & 0x0FFF
        self.index = address

    def OP_BNNN(self):
        address = self.opcode & 0x0FFF
        self.pc = self.registers[0]+address

    def OP_CXKK(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        byte = self.opcode & 0x00FF

        self.registers[Vx] = int(random()*255) & byte

    def OP_DXYN(self):
        xCoord = 0
        yCoord = 0
        nVal = self.opcode & 0x000F
        Vx = (self.opcode & 0x0F00) >> 8
        Vy = (self.opcode & 0x00F) >> 4
        while xCoord<8:
            while yCoord<=nVal:
                pixel = (self.memory[self.index+yCoord] >> (7-xCoord)) & 1
                screenY = ((yCoord+self.registers[Vy])%self.HEIGHT)
                screenX = ((xCoord+self.registers[Vx])%self.WIDTH)
                xorVal = self.video[screenY][screenX] ^ pixel
                if xorVal == 1:
                    self.video[screenY][screenX] = 1
                    self.registers[0xF] = 0
                elif xorVal == 0:
                    self.video[screenY][screenX] = 0
                    self.registers[0xF] = 1
                yCoord+=1
            xCoord+=1
        print("Drew")

    def OP_EX9E(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        key = self.registers[Vx]

        if self.KeyPad[key]:
            pc+=2

    def OP_EXA1(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        key = self.registers[Vx]

        if not self.KeyPad[key]:
            pc+=2

    def OP_FX07(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        self.registers[Vx] = self.delayTimer

    def OP_FX0A(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8

        if keyPad[0]:
            registers[Vx] = 0
        elif keyPad[1]:
            registers[Vx] = 1
        elif keyPad[2]:
            registers[Vx] = 2
        elif keyPad[3]:
            registers[Vx] = 3
        elif keyPad[4]:
            registers[Vx] = 4
        elif keyPad[5]:
            registers[Vx] = 5
        elif keyPad[6]:
            registers[Vx] = 6
        elif keyPad[7]:
            registers[Vx] = 7
        elif keyPad[8]:
            registers[Vx] = 8
        elif keyPad[9]:
            registers[Vx] = 9
        elif keyPad[10]:
            registers[Vx] = 10
        elif keyPad[11]:
            registers[Vx] = 11
        elif keyPad[12]:
            registers[Vx] = 12
        elif keyPad[13]:
            registers[Vx] = 13
        elif keyPad[14]:
            registers[Vx] = 14
        elif keyPad[15]: 
            registers[Vx] = 15
        else:
            pc-=2

    def OP_FX15(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        self.delayTimer = self.registers[Vx]

    def OP_FX18(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        self.soundTimer = self.registers[Vx]

    def OP_FX1E(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        self.index += self.registers[Vx]

    def OP_FX29(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        digit = self.registers[Vx]

        self.index = self.FONTSET_START_ADDRESS + (5 * digit)

    def OP_FX33(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        value = self.registers[Vx]

        self.memory[self.index+2] = self.value%10
        self.value /= 10

        self.memory[index+1] = value%10
        self.value /= 10

        self.memory[index] = self.value%10

    def OP_FX55(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        i =0
        while i<=Vx:
            self.memory[self.index+i] = self.registers[i]
            i+=1

    def OP_FX65(self):
        Vx = (self.memory[self.pc] & 0x0F00) >> 8
        i =0
        while i<=Vx:
            self.memory[i] = self.registers[self.index+i]
            i+=1

    def RunInscruction(self, opcode):
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x0F00) >> 4

        if (opcode & 0xF000) == 0x0000:
            if opcode == 0x00E0:
                print(f"Calling opcode: {opcode}, Name:00E0, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_00E0()
            elif opcode == 0x00EE:
                print(f"Calling opcode: {opcode}, Name:00EE, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_00EE()
            pass
        elif (opcode & 0xF000) == 0x1000:
            print(f"Calling opcode: {opcode}, Name:1NNN, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
            self.OP_1NNN()
        elif (opcode & 0xF000) == 0x2000:
            print(f"Calling opcode: {opcode}, Name:2NNN, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
            self.OP_2NNN()
        elif (opcode & 0xF000) == 0x3000:
            print(f"Calling opcode: {opcode}, Name:3XKK, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
            self.OP_3XKK()
        elif (opcode & 0xF000) == 0x4000:
            print(f"Calling opcode: {opcode}, Name:4XKK, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
            self.OP_4XKK()
        elif (opcode & 0xF000) == 0x5000:
            print(f"Calling opcode: {opcode}, Name:5XY0, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
            self.OP_5XY0()
        elif (opcode & 0xF000) == 0x6000:
            print(f"Calling opcode: {opcode}, Name:6XKK, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
            self.OP_6XKK()
        elif (opcode & 0xF000) == 0x7000:
            print(f"Calling opcode: {opcode}, Name:7XKK, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
            self.OP_7XKK()
        elif (opcode & 0xF000) == 0x8000:
            if (opcode & 0xF) == 0x0:
                print(f"Calling opcode: {opcode}, Name:8XY0, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_8XY0()
            elif opcode == 0x1:
                print(f"Calling opcode: {opcode}, Name:8XY1, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_8XY1()
            elif opcode == 0x2:
                print(f"Calling opcode: {opcode}, Name:8XY2, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_8XY2()
            elif opcode == 0x3:
                print(f"Calling opcode: {opcode}, Name:8XY3, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_8XY3()
            elif opcode == 0x4:
                print(f"Calling opcode: {opcode}, Name:8XY4, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_8XY4()
            elif opcode == 0x5:
                print(f"Calling opcode: {opcode}, Name:8XY5, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_8XY5()
            elif opcode == 0x6:
                print(f"Calling opcode: {opcode}, Name:8XY6, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_8XY6()
            elif opcode == 0x7:
                print(f"Calling opcode: {opcode}, Name:8XY7, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_8XY7()
            elif opcode == 0xE:
                print(f"Calling opcode: {opcode}, Name:8XY8, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_8XYE()
            pass
        elif (opcode & 0xF000) == 0x9000:
            print(f"Calling opcode: {opcode}, Name:9XY0, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
            self.OP_9XY0()
        elif (opcode & 0xF000) == 0xA000:
            print(f"Calling opcode: {opcode}, Name:ANNN, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
            self.OP_ANNN()
        elif (opcode & 0xF000) == 0xB000:
            print(f"Calling opcode: {opcode}, Name:BNNN, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
            self.OP_BNNN()
        elif (opcode & 0xF000) == 0xC000:
            print(f"Calling opcode: {opcode}, Name:CXKK, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
            self.OP_CXKK()
        elif (opcode & 0xF000) == 0xD000:
            print(f"Calling opcode: {opcode}, Name:DXYN, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
            self.OP_DXYN()
        elif (opcode & 0xF000) == 0xE000:
            if (opcode & 0xF) == 0x9E:
                print(f"Calling opcode: {opcode}, Name:EX9E, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_EX9E()
            elif (opcode & 0xF) == 0xA1:
                print(f"Calling opcode: {opcode}, Name:EXA1, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_EXA1()
            pass
        elif (opcode & 0xF000) == 0xF000:
            if (opcode & 0xF) == 0x07:
                print(f"Calling opcode: {opcode}, Name:FX07, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_FX07()
            elif (opcode & 0xF) == 0x0A:
                print(f"Calling opcode: {opcode}, Name:FX0A, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_FX0A()
            elif (opcode & 0xF) == 0x15:
                print(f"Calling opcode: {opcode}, Name:FX15, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_FX15()
            elif (opcode & 0xF) == 0x18:
                print(f"Calling opcode: {opcode}, Name:FX18, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_FX18()
            elif (opcode & 0xF) == 0x1E:
                print(f"Calling opcode: {opcode}, Name:FX1E, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_FX1E()
            elif (opcode & 0xF) == 0x29:
                print(f"Calling opcode: {opcode}, Name:FX29, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_FX29()
            elif (opcode & 0xF) == 0x33:
                print(f"Calling opcode: {opcode}, Name:FX33, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_FX33()
            elif (opcode & 0xF) == 0x55:
                print(f"Calling opcode: {opcode}, Name:FX55, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_FX55()
            elif (opcode & 0xF) == 0x65:
                print(f"Calling opcode: {opcode}, Name:FX65, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
                self.OP_FX65()
        else:
            print(f"Unknown opcode: {opcode}, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")

    def Cycle(self):
        self.opcode = (self.memory[self.pc]<<8) | self.memory[self.pc+1]
        self.pc+=2
        self.RunInscruction(self.opcode)
        if self.delayTimer > 0:
            self.delayTimer -= 1

        if self.soundTimer > 0:
            self.soundTimer -= 1