import pygame
from random import random
import numpy as np

def DrawPixel(surface, Pixelcolor, pos, scale):
    pygame.draw.rect(surface, Pixelcolor, pygame.Rect(pos[0], pos[1], scale, scale)) 


class Screen:
	def __init__(self,size, upscalling=10):
		self.x = size[0]
		self.y = size[1]
		self.grid = [[0 for i in range(64)] for j in range(32)] 
		self.grid = np.array(self.grid).T

		self.upscalling = upscalling

		self.design = pygame.Surface([self.x, self.y])
		self.window = pygame.display.set_mode([self.x*upscalling+200, self.y*upscalling+200])

	def setPixel(self, coordinates, data, xor=False):
		x = int(coordinates/self.x)
		y = int(coordinates%self.x)-1
		xFloat = coordinates/self.x
		yFloat = coordinates%self.x

		print((x,y),(xFloat, yFloat))

		if xor:
			self.grid[x][y] ^= data
		else:
			self.grid[x][y] = data

	def getPixel(self, coordinates):
		x = int(coordinates/self.x)
		y = int(coordinates%self.x)-1
		xFloat = coordinates/self.x
		yFloat = coordinates%self.x

		return self.grid[x][y]

	def draw(self):

		for i in range(2047):
			x = int(i%self.x)
			y = int(i/self.x)

			color = 0

			# print(x, y, len(self.grid), len(self.grid[0]))
			pixel = self.grid[x][y]
			if pixel == 0:
				color = (0, 0, 0)
			elif pixel == 1:
				color = (200, 200, 200)
			# print(f"X: {x}, Y: {y}, Index: {i}, Color: {color}")

			DrawPixel(self.design, color, (x, y), 1)
		frame = pygame.transform.scale(self.design, (640, 320))
		self.window.blit(frame, frame.get_rect())
		pygame.display.flip()

	def DebugDraw(self):
		pass

	def clear(self):
		self.grid = [[0 for i in range(64)] for j in range(32)] 
		self.grid = np.array(self.grid).T

	def clearDebug(self):
		pass

	def __repr__(self):
		self.grid = self.grid
		return str(self.grid)

class CHIP8:
	def __init__(self):
		# self.lookupTable = {0x0000:{"mask":0xFFFF,0x00E0:self.OP_00E0,0x00EE:self.OP_00EE},0x1000:self.OP_1NNN,0x2000:self.OP_2NNN,0x3000:self.OP_3XNN,0x4000:self.OP_4XNN,0x5000:self.OP_5XY0,0x6000:self.OP_6XNN,0x7000:self.OP_7XNN,0x8000:{"mask":0xF,0x0:self.OP_8XY0,0x1:self.OP_8XY1,0x2:self.OP_8XY2,0x3:self.OP_8XY3,0x4:self.OP_8XY4,0x5:self.OP_8XY5,0x6:self.OP_8XY6,0x7:self.OP_8XY7,0xE:self.OP_8XYE},0x9000:self.OP_9XY0,0xA000:self.OP_ANNN,0xB000:self.OP_BNNN,0xC000:self.OP_CXNN,0xD000:self.OP_DXYN,0xE000:{"mask":0xFF,0x9E:self.OP_EX9E,0xA1:self.OP_EXA1},0xF000:{"mask":0xFF,0x07:self.OP_FX07,0x0A:self.OP_FX0A,0x15:self.OP_FX15,0x18:self.OP_FX18,0x1E:self.OP_FX1E,0x29:self.OP_FX29,0x33:self.OP_FX33,0x55:self.OP_FX55,0x65:self.OP_FX65}}

		#Init variables
		self.opcode = 0
		self.memory = [0]*4096
		self.V = [0]*16
		self.I = 0
		self.pc = 0x200
		self.sp = 0x0
		self.graphics = Screen((64, 32))
		self.fontSet = [
		0xF0, 0x90, 0x90, 0x90, 0xF0,
		0x20, 0x60, 0x20, 0x20, 0x70,
		0xF0, 0x10, 0xF0, 0x80, 0xF0,
		0xF0, 0x10, 0xF0, 0x10, 0xF0,
		0x90, 0x90, 0xF0, 0x10, 0x10,
		0xF0, 0x80, 0xF0, 0x10, 0xF0,
		0xF0, 0x80, 0xF0, 0x90, 0xF0,
		0xF0, 0x10, 0x20, 0x40, 0x40,
		0xF0, 0x90, 0xF0, 0x90, 0xF0,
		0xF0, 0x90, 0xF0, 0x10, 0xF0,
		0xF0, 0x90, 0xF0, 0x90, 0x90,
		0xE0, 0x90, 0xE0, 0x90, 0xE0,
		0xF0, 0x80, 0x80, 0x80, 0xF0,
		0xE0, 0x90, 0x90, 0x90, 0xE0,
		0xF0, 0x80, 0xF0, 0x80, 0xF0,
		0xF0, 0x80, 0xF0, 0x80, 0x80
		]
		self.delayTimer = 0
		self.soundTimer = 0
		self.stack = [0]*16
		self.key = [0]*16
		self.drawFlag = True

		#Code
		for i in range(80):
			self.memory[i] = self.fontSet[i]

	def loadROM(self, path):
		file = open(path, "rb").read()
		bufferSize = len(file)
		i = 0
		while i < bufferSize:
			self.memory[i+0x200] = file[i]
			i += 1

	def OP_00E0(self):
		self.graphics.clear()
		return None

	def OP_00EE(self):
		pass

	def OP_1NNN(self ,nnn):
		pc = nnn

	def OP_2NNN(self):
		pass

	def OP_3XNN(self):
		pass

	def OP_4XNN(self):
		pass

	def OP_5XY0(self):
		pass

	def OP_6XNN(self, nn, Vx):
		self.V[Vx] = nn

	def OP_7XNN(self, nn, Vx):
		self.V[Vx] += nn

	def OP_8XY0(self):
		pass

	def OP_8XY1(self):
		pass

	def OP_8XY2(self):
		pass

	def OP_8XY3(self):
		pass

	def OP_8XY4(self):
		pass

	def OP_8XY5(self):
		pass

	def OP_8XY6(self):
		pass

	def OP_8XY7(self):
		pass

	def OP_8XYE(self):
		pass

	def OP_9XY0(self):
		pass

	def OP_ANNN(self, nnn):
		self.I = nnn

	def OP_BNNN(self):
		pass

	def OP_CXNN(self):
		pass

	def OP_DXYN(self, Vx, Vy, n):
		print("Drawing")
		self.V[0xF] = 0
		x = self.V[Vx] & 0xFF
		y = self.V[Vy] & 0xFF
		height = n
		row = 0

		while row < height:
		 	currRow = self.memory[row+self.I]
		 	column = 0
		 	while column < 8:
		 		loc = x + column + ((y + row) * 64)
		 		column += 1
		 		if (y + row) >= 32 or (x + column - 1) >= 64:
		 			continue
		 		mask = 1 << 8-column
		 		pixel = (currRow & mask) >> (8 - column)
		 		self.graphics.setPixel(loc, pixel, True)
		 		if self.graphics.getPixel(loc) == 0:
		 			self.V[0xF] = 1
		 		else:
		 			self.V[0xF] = 0
		 	row += 1
		print("Drew")
		self.drawFlag = True

	def OP_EX9E(self):
		pass

	def OP_EXA1(self):
		pass

	def OP_FX07(self):
		pass

	def OP_FX0A(self):
		pass

	def OP_FX15(self):
		pass

	def OP_FX18(self):
		pass

	def OP_FX1E(self):
		pass

	def OP_FX29(self):
		pass

	def OP_FX33(self):
		pass

	def OP_FX55(self):
		pass

	def OP_FX65(self):
		pass

	def OP_00CN(self):
		pass

	def OP_00FB(self):
		pass

	def OP_00FC(self):
		pass

	def OP_00FD(self):
		pass

	def OP_00FE(self):
		pass

	def OP_00FF(self):
		pass

	def OP_DXY0(self):
		pass

	def OP_FX30(self):
		pass

	def OP_FX75(self):
		pass

	def OP_FX85(self):
		pass

	def drawText(self, coords, text):
		pass

	def execute(self):
		self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc+1]
		opcode = self.memory[self.pc] << 8 | self.memory[self.pc+1]

		x = (self.opcode & 0x0f00) >> 8
		y = (self.opcode & 0x00f0) >> 4
		n = self.opcode & 0x000F
		nn = self.opcode & 0x00FF
		nnn = self.opcode & 0x0FFF

		if (opcode & 0xF000) == 0x0000:
			if opcode == 0x00E0:
				print(f"Calling opcode: {opcode}, Name:00E0, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
				self.OP_00E0()
			elif opcode == 0x00EE:
				print(f"Calling opcode: {opcode}, Name:00EE, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
				self.OP_00EE()
		elif (opcode & 0xF000) == 0x1000:
			print(f"Calling opcode: {opcode}, Name:1NNN, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
			self.OP_1NNN(nnn)
		elif (opcode & 0xF000) == 0x2000:
			print(f"Calling opcode: {opcode}, Name:2NNN, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
			self.OP_2NNN()
		elif (opcode & 0xF000) == 0x3000:
			print(f"Calling opcode: {opcode}, Name:3XKK, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
			self.OP_3XNN()
		elif (opcode & 0xF000) == 0x4000:
			print(f"Calling opcode: {opcode}, Name:4XKK, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
			self.OP_4XNN()
		elif (opcode & 0xF000) == 0x5000:
			print(f"Calling opcode: {opcode}, Name:5XY0, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
			self.OP_5XY0()
		elif (opcode & 0xF000) == 0x6000:
			print(f"Calling opcode: {opcode}, Name:6XKK, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
			self.OP_6XNN(x, nn)
		elif (opcode & 0xF000) == 0x7000:
			print(f"Calling opcode: {opcode}, Name:7XKK, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
			self.OP_7XNN(x, nn)
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
		elif (opcode & 0xF000) == 0x9000:
			print(f"Calling opcode: {opcode}, Name:9XY0, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
			self.OP_9XY0()
		elif (opcode & 0xF000) == 0xA000:
			print(f"Calling opcode: {opcode}, Name:ANNN, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
			self.OP_ANNN(nnn)
		elif (opcode & 0xF000) == 0xB000:
			print(f"Calling opcode: {opcode}, Name:BNNN, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
			self.OP_BNNN()
		elif (opcode & 0xF000) == 0xC000:
			print(f"Calling opcode: {opcode}, Name:CXKK, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
			self.OP_CXKK()
		elif (opcode & 0xF000) == 0xD000:
			print(f"Calling opcode: {opcode}, Name:DXYN, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
			self.OP_DXYN(x, y, n)
		elif (opcode & 0xF000) == 0xE000:
			if (opcode & 0xF) == 0x9E:
				print(f"Calling opcode: {opcode}, Name:EX9E, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
				self.OP_EX9E()
			elif (opcode & 0xF) == 0xA1:
				print(f"Calling opcode: {opcode}, Name:EXA1, Group: {(opcode & 0xF000) >> 12}, X: {(opcode & 0x0F00) >> 8}, Y: {(opcode & 0x00F0) >> 4}, N: {opcode & 0x000F}, NN: {opcode & 0x00FF}, NNN: {opcode & 0x0FFF}")
				self.OP_EXA1()
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

		pc += 2

		if self.delayTimer > 0:
			self.delayTimer -= 1

		if self.soundTimer > 0:
			if self.soundTimer == 1:
				print('Beep')
			self.soundTimer -= 1

	def cycle(self):
		clock = pygame.time.Clock()
		while True:
			clock.tick(60)
			try:
				self.execute()
			except:
				break

	def start(self):
		clock = pygame.time.Clock()
		done = False
		while not done:
			clock.tick(60)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
			
			self.cycle()
			if self.drawFlag:
				self.graphics.draw()
				self.drawFlag = False

chip8 = CHIP8()
chip8.loadROM("./IBM Logo.ch8")

chip8.start()
