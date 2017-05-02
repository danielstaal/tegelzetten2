'''
Main running file
Date: 
Daniel Staal


'''

import math
import copy
import time
from itertools import repeat
from itertools import permutations
from random import randint
from random import shuffle
import sys
import csv
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import copy

import Grid

def solve_borders(all_blocks, length, width):
	# create the initial empty grid
	emptygrid = Grid.Grid(length, width, all_blocks)
	# initialize the expandable worlds with the empty grid
	worlds = [emptygrid]
	# a list to store completed worlds
	complete_worlds = []

	# This function is designed to make sure mirror worlds dont exist
	worlds = place_first_block(worlds)

	# for i in range(20):
	i = 0
	while len(worlds) != 0:
		i += 1
		print('Blocks in the grid: ', i)
		[worlds, complete] = expand_worlds(worlds) 

		if len(complete) > 0:
			complete_worlds.extend(complete)

	return [worlds, complete_worlds]

def place_first_block(worlds):
	empty_world = worlds[0]

	block, block_no = get_largest_block(empty_world)

	new_worlds = []

	max_positions = math.floor(empty_world.length)/2
	if block[0] % 2 == 0:
		max_positions += 1
	half_block = math.floor(block[0]/2)
	index = 0
	# to get all possible placements without mirrors
	while index + half_block < max_positions:
		world_copy = copy.deepcopy(empty_world)
		world_copy.place_first_block(block, index)
		new_worlds.append(world_copy)
		index += 1

	# remove the block from the list of blocks
	empty_world.blocks[block_no].remove(block)
	empty_world.no_of_blocks -= 1

	return new_worlds

def get_largest_block(world):
	blocks = world.blocks

	largest = 100000
	largest_i = -1

	for i, block in enumerate(blocks):
		size = block[0][0]*block[0][1]
		if size > largest:
			largest = size
			largest_i = i
	return world.blocks[i][0], i

def expand_worlds(worlds):
	new_complete = []
	new_worlds = []
	print('Amount of worlds to expand:', len(worlds))
	for possible_world in worlds:
		# print(possible_world.grid)
		# print(possible_world.blocks)
		block_no = 0
		max_block_no = possible_world.no_of_different_blocks
		# flag == 0 means a block is placed in a new world
		# flag == 1 means a block is placed and border is filled
		# flag == 2 means no more options and not complete
		flag = 0
		while (flag == 0 or flag == 1) and block_no < max_block_no:
			# print('tries:', tries)
			world_copy = copy.deepcopy(possible_world)
			flag, skip = world_copy.add_block(block_no)
			block_no += skip
			# print('flag:',flag)
			if flag == 0:
				new_worlds.append(world_copy)
			elif flag == 1:
				new_complete.append(world_copy)
			block_no += 1

		# if flag == 2:
			# print('no more possibilities')
			# print(possible_world.grid)

	# remove mirrored worlds
	# new_worlds = check_mirrors(new_worlds)
	# new_complete = check_mirrors(new_complete)

	return [new_worlds, new_complete]

# def check_mirrors(worlds):

# 	non_mirror_worlds = []
# 	no_of_worlds = len(worlds)
# 	# get the actual grids
# 	grids = []
# 	for i, world in enumerate(worlds):
# 		grids.append(world.grid.all())

# 	while len(worlds) > 0:
# 		world = worlds.pop(0)
# 		non_mirror_worlds.append(world)

# 		mirrors = [world.grid, np.fliplr(world.grid), np.flipud(world.grid), np.fliplr(np.flipud(world.grid))]
# 		# remove the mirrors from new_worlds
# 		for i in range(len(mirrors)):
# 			for j, other_world in enumerate(worlds):
# 				if (other_world.grid==mirrors[i]).all():
# 					del worlds[j]
# 	print('Deleted mirrors:', no_of_worlds - len(non_mirror_worlds))
# 	return non_mirror_worlds

if __name__ == '__main__':
	# initializing the blocks
	# set_of_blocks = [[1,1],[2,2],[4,4], [3,3], [5,5], [2,8], [1,1]]
	set_of_blocks = [[[1,1], [1,1]], [[2,2], [2,2], [2,2], [2,2], [2,2], [2,2], [2,2], [2,2]],
	 [[4,4],[4,4]]]

	# set_of_blocks = [[[3,3]]*20]
	# set_of_blocks.append([[2,2]]*5)
	# print(set_of_blocks)
	[no_solutions, solutions] = solve_borders(set_of_blocks, 8, 8)
	print(no_solutions)
	print(solutions)
	print('no of non-solutions: ', len(no_solutions))
	
	# for world in no_solutions:
	# 	print(world.grid)

	print('no of solutions: ', len(solutions))
	my_cmap = cm.get_cmap('YlGnBu')
	my_cmap.set_bad('white')

	for i, sol in enumerate(solutions[0:10]):
		plt.figure(i+1)
		plt.imshow(sol.grid, cmap=my_cmap, interpolation='none')
	plt.show()
	
