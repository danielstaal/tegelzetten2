import math
from random import randint
import numpy as np
import copy

class Grid:
	def __init__(self, length, width, blocks):
		self.blocks = blocks
		self.no_of_different_blocks = len(self.blocks)
		self.length = length
		self.width = width
		self.grid = np.zeros((length, width))
		self.current_location = [0,0]
		self.no_of_blocks = 0
		# count the blocks of each size
		for block in blocks: 
			self.no_of_blocks += len(block)

		self.side = 0

	def place_first_block(self, first_block, index):
		x = 0
		y = index
		x2 = first_block[0]
		y2 = y + first_block[1]

		self.update_grid(x, x2, y, y2, first_block)

	def add_block(self, block_no):
		new_worlds = []
		complete_worlds = []

		# print(block_no)
		# print(self.no_of_different_blocks)
		# print('from', block_no, 'to', self.no_of_different_blocks)
		# amount of blocks to skip
		skip = 0
		for i in range(block_no, self.no_of_different_blocks):
			# check if not out of bounds because of removing a list in
			# place_in_grid and decreasing self.no_of_different_blocks

			# print(self.blocks)
			# print(self.blocks[i][0])
			flag = self.place_in_grid(self.blocks[i][0], i)
			if flag == 0 or flag == 1:
				# remove empty lists
				self.blocks = [x for x in self.blocks if x != []]
				self.no_of_different_blocks = len(self.blocks)
				# print('block placed')
				# print('skip', skip)
				# print('flag', flag)
				return flag, skip
			else:
				skip += 1
				# print('block failed')
		return 2, 0

	def place_in_grid(self, block, i):
		x = self.current_location[0]
		y = self.current_location[1]
		x2 = x+block[0]
		y2 = y+block[1]

		if self.side == 1:
			y -= block[1]
			y2 -= block[1]
		if self.side == 2:
			y -= block[1]-1
			y2 -= block[1]-1
			x -= block[0]
			x2 -= block[0]

		# print('coors:', x, x2, y, y2)
		# print(block)
		# print('before:\n', self.grid)
		if(x >= 0 and x2 < self.length+1 and y >= 0 and y2 < self.width+1):
			if not self.update_grid(x, x2, y, y2, block):
				return 2
			# block succesfully put in grid then:
			else:
				# if len(self.blocks[i]) == 1:
					# del self.blocks[i]
					# self.no_of_different_blocks -= 1
				# else:
				self.blocks[i].remove(block)
				self.no_of_blocks -= 1
				# and always update
				return self.update_current_location()

	def update_grid(self, x, x2, y, y2, block):
		# check overlap
		# print(self.grid)
		# print('coors:', x, x2, y, y2)		# 
		if np.amax(self.grid[x:x2, y:y2]) > 0:
			# print('overlap')
			return False
		else:
			# print('coors:', x, x2, y, y2)
			self.grid[x:x2, y:y2] += block[0]
			# print('after: \n',self.grid)	
			# print(self.grid)
			return True
		
	def update_current_location(self):
		# print(self.grid)
		while self.side < 4:
			# print('side:', self.side)
			side_vector = []
			if self.side == 0:
				side_vector = self.grid[0, :]
			elif self.side == 1:
				side_vector = self.grid[:, -1]
			elif self.side == 2:
				side_vector = self.grid[-1, :]
			elif self.side == 3:
				side_vector = self.grid[:, 0]
			# print(side_vector)	
			# print(self.current_location)	
			locate_zero = np.where(side_vector==0)
			if len(locate_zero[0]) > 0: 
				loc = 0
				# take the last index for the bottom side
				if self.side == 2:
					loc = locate_zero[0][-1]
				else:
					loc = locate_zero[0][0]
				self.current_location = self.get_location(loc)
				# print('newloc:', self.current_location)
				return 0
			else:
				# print(len(locate_zero[0]))
				self.side += 1
		return 1

	def get_location(self, index):
		if self.side == 0:
			return [0, index]
		if self.side == 1:
			return [index, self.width]
		if self.side == 2:
			return [self.length, index]
		else:
			return [index, 0]
		