import numpy as np
from itertools import product as iterprod, permutations as iterperm

class Cage:

	def __init__(self, rule, coords):
		self.rule = rule # [0] value goal, [1] operation
		self.coords = coords

		self.combinations = []
		self.digits = []
		self.solution_sets = []

	def __repr__(self):
		return 'Cage({}, {})'.format(self.rule, self.coords)

	def calc_combination(self, items):
		operation = self.rule[1]

		if operation == '+':
			return sum(items)
		elif operation == '-': # will only be two items
			return abs(items[0] - items[1])
		elif operation == '*':
			x = items[0]
			for i in items[1:]:
				x *= i
			return x
		elif operation == '/': # will only be two items
			x = items[0] / items[1]
			if x < 1:
				x = items[1] / items[0]
			if x.is_integer(): # make sure no remainder
				return x
			else:
				return 0

	def calc_combinations(self, m):
		if len(self.coords) == 1:
			possible_combinations = [tuple([self.rule[0]])]
		else:
			all_combinations = list(iterprod(range(1, m+1), repeat=len(self.coords)))

			possible_combinations = []
			for comb in all_combinations:
				comb = tuple(comb)
				result = self.calc_combination(comb)
				if result == self.rule[0]:
					possible_combinations.append(comb)

		self.combinations = possible_combinations
		self.digits = list(set([x for y in possible_combinations for x in y]))

	def calc_solution_sets(self):
		for combination in self.combinations:
			self.solution_sets.append(list(zip(self.coords, combination)))


def import_puzzle(file_name):

	# import file
	file = open(file_name, 'r')
	file_lines = [line for line in file]

	# create 'cage_grid' array
	cage_grid = [[int(value) for value in line] for line in [grid_line[:-1].split() for grid_line in file_lines[:-1]]]
	m = len(cage_grid[0])
	rule_string_sets = [[a[:-1], a[-1]] for a in file_lines[-1].split()]
	
	# create 'rules' list
	rules = []
	for rule_string in rule_string_sets:
		if rule_string[0] == '': # no operator; use sum with single-digit
			rules.append([int(rule_string[1]), '+'])
		else:
			rules.append([int(rule_string[0]), rule_string[1]])

	# create 'cages' list
	cages = []
	for j, line in enumerate(cage_grid):
		for i, cage_index in enumerate(line):
			try:
				cages[cage_index].coords.append((i, j))
			except IndexError:
				cages.append(Cage(rules[cage_index], [(i, j)]))

	return cage_grid, rules, cages, m

def draw_puzzle(grid):
	for row in grid:
		a = []
		for i in row:
			if i == None or i == 0:
				a.append('.')
			else:
				a.append(str(int(i)))

		print(" ".join(a))

def apply_solution_set_to_grid(solution_set, grid):
	for solution in solution_set:
		x, y = solution[0][0], solution[0][1]
		value = solution[1]
		grid[x][y] = value

if __name__ == '__main__':
	cage_grid, rules, cages, m = import_puzzle('puzzle.txt')

	# form combinations and solution sets
	for cage in cages:
		cage.calc_combinations(m)
		cage.calc_solution_sets()

	# create grid
	grid = np.zeros((m, m))

	solution_set_index_ref = []
	for cage in cages: 
		l = list(range(len(cage.solution_sets)))
		solution_set_index_ref.append(l)

	answers_checked = 0
	answer_found = False
	answer = [0]*len(solution_set_index_ref)
	a = 0

	while not answer_found:
		print('Testing:', answer)

		# test answer for legality
		legal = True
		for cage_idx, sol_idx in enumerate(answer):
			apply_solution_set_to_grid(cages[cage_idx].solution_sets[sol_idx], grid)

			# TODO: LEGALLITY CHECK
			if True:
				legal = False
				break

		if legal: # found correct answer
			answer_found = True
			break
		else: # didn't find correct answer, iterate to next answer
			answers_checked += 1
			print('NOT LEGAL (#{})'.format(answers_checked))
			for i in range(len(solution_set_index_ref)):
				lim = len(solution_set_index_ref[i])-1
				if answer[i] >= lim:
					answer[i] = 0 
				else:
					answer[i] += 1
					break

		draw_puzzle(grid)