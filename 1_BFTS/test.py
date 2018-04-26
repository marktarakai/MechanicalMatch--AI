import time
import copy
from collections import deque

class Grid:
	quota = 0
	gridWidth = 0 
	gridHeight = 0
	poolHeight = 0
	numTypes = 0
	maxSwaps = 0
	matrix = []
	def __init__(self, quota, width, pHeight, gHeight, grid, types, swaps):
		self.quota = quota
		self.gridWidth = width
		self.poolHeight = pHeight
		self.gridHeight = gHeight
		self.matrix = [[int(j) for j in i] for i in grid]
		self.numTypes = types
		self.maxSwaps = swaps

	def checkMatches(self):
		tempSet = deque()
		finalSet = deque()
		tempScore = 1
		#check matches in rows
		for x in range(self.poolHeight, self.gridHeight):
			tempSet.clear()
			tempScore = 1
			for y in range(self.gridWidth - 1):
				if(self.matrix[x][y] == self.matrix[x][y+1]):
					tempScore = tempScore + 1
					if((x,y) not in tempSet):
						tempSet.append((x,y))
						tempSet.append((x,y+1))
					else:
						tempSet.append((x,y+1))
					if(tempScore > 2 and y + 1 == self.gridWidth - 1):
						for item in tempSet:
							finalSet.append(item)
						tempSet.clear()
						tempScore = 1
				elif(tempScore > 2):
					for item in tempSet:
						finalSet.append(item)
					tempSet.clear()
					tempScore = 1
				else:
					tempSet.clear()
					tempScore = 1
		#check matches in columns
		for y in range(self.gridWidth):
			tempSet.clear()
			tempScore = 1
			for x in range(self.poolHeight, self.gridHeight - 1):
				if(self.matrix[x][y] == self.matrix[x+1][y]):
					tempScore = tempScore + 1
					if((x,y) not in tempSet):
						tempSet.append((x,y))
						tempSet.append((x+1,y))
					else:
						tempSet.append((x+1,y))
					if(tempScore > 2 and x + 1 == self.gridHeight - 1):
						for item in tempSet:
							finalSet.append(item)
						tempSet.clear()
						tempScore = 1
				elif(tempScore > 2):
					for item in tempSet:
						finalSet.append(item)
					tempSet.clear()
					tempScore = 1
				else:
					tempSet.clear()
					tempScore = 1
		return finalSet

	def checkSwaps(self):
		mySet = deque()
		#check horizontal swaps
		for x in range(self.poolHeight, self.gridHeight):
			for y in range(self.gridWidth - 1):
				self.matrix[x][y], self.matrix[x][y+1] = self.matrix[x][y+1], self.matrix[x][y]
				if(len(self.checkMatches()) > 0):
					mySet.append((x,y,x,y+1))
				self.matrix[x][y], self.matrix[x][y+1] = self.matrix[x][y+1], self.matrix[x][y]
		#check verticle swaps
		for y in range(self.gridWidth):
			for x in range(self.poolHeight, self.gridHeight - 1):
				self.matrix[x][y], self.matrix[x+1][y] = self.matrix[x+1][y], self.matrix[x][y]
				if(len(self.checkMatches()) > 0):
					mySet.append((x,y,x+1,y))
				self.matrix[x][y], self.matrix[x+1][y] = self.matrix[x+1][y], self.matrix[x][y]
		return mySet

	def clearBoard(self, matches):
		while(len(matches) != 0):
			match = matches.pop()
			self.matrix[match[0]][match[1]] = 0

	def fillAbove(self, row, column, replaced):
		while(row > 0):
			self.matrix[row][column] = self.matrix[row-1][column]
			row = row - 1
		self.matrix[0][column] = (((column + self.matrix[1][column]) + replaced) % self.numTypes) + 1

	def fillBoard(self):
		replaced = 0
		for x in range(self.poolHeight, self.gridHeight):
			for y in range(self.gridWidth):
				if(self.matrix[x][y] == 0):
					replaced = replaced + 1
					self.fillAbove(x, y, replaced)
		return replaced

	def swap(self, swapCoord):
		self.matrix[swapCoord[0]][swapCoord[1]], self.matrix[swapCoord[2]][swapCoord[3]] = self.matrix[swapCoord[2]][swapCoord[3]], self.matrix[swapCoord[0]][swapCoord[1]]

	def stabilizeBoard(self):
		tempScore = 0
		while(len(self.checkMatches()) > 0):
			self.clearBoard(self.checkMatches())
			tempScore = tempScore + self.fillBoard()
		return tempScore

	def results(self, swapCoord):
		state = State()
		newGrid = copy.deepcopy(self)
		newGrid.swap(swapCoord)
		state.score = copy.deepcopy(newGrid.stabilizeBoard())
		state.grid = copy.deepcopy(newGrid)
		state.grid.matrix = copy.deepcopy(newGrid.matrix)
		return state

class State:
	grid = None
	score = 0

	def actions(self):
		newGrid = copy.deepcopy(self)
		newGrid.grid.checkSwaps()

class Node:
	state = State()
	parent = None
	action = None
	pathCost = 0

	def childNode(self, node, action):
		cNode = Node()
		cNode.state = copy.deepcopy(node.state.grid.results(action))
		cNode.state.score = copy.deepcopy(node.state.score + cNode.state.score)
		cNode.parent = copy.deepcopy(node)
		cNode.pathCost = copy.deepcopy(node.pathCost + 1)
		cNode.action = action
		return cNode

def breadthFirstSearch(node):
	if(node.state.score >= node.state.grid.quota):
		return node
	frontier = deque()
	frontier.append(node)
	while(len(frontier) > 0):
		currentNode = frontier.popleft()
		if(currentNode.pathCost <= currentNode.state.grid.maxSwaps):
			for action in currentNode.state.grid.checkSwaps():
				child = currentNode.childNode(currentNode, action)
				if (child.state.score >= child.state.grid.quota):
					return child
				frontier.append(child)
		else:
			print('No Solution: Swap Limit Reached')
			return
	print('No Solution')
	return

def getSolutionPath(node):
	path = deque()
	while(node.parent != None):
		path.appendleft(node.action)
		node = node.parent
	return path


#parse very first matrix from given input file to a 2d list
def initMatrix(numbers, height):
	grid = []
	for y in range(height):
		row = (myVars[y + 7].split())
		grid.append(row)
	return grid

def printSolution(deque):
	while(len(deque) > 0):
		print('(' + str(deque[0][1]) + ',' + str(deque[0][0]) + '),(' + str(deque[0][3]) + ',' + str(deque[0][2]) + ')')
		deque.popleft()

t0 = time.clock()
with open('puzzle1.txt', 'r') as f:
	myVars = f.read().splitlines()



#grab variables from input file
quota = int(myVars[0])
maxSwaps = int(myVars[1])
numTypes = int(myVars[2])
gridWidth = int(myVars[3])
gridHeight = int(myVars[4])
poolHeight = int(myVars[5])
bonusRule = int(myVars[6])
myGrid = initMatrix(myVars, gridHeight)

grid = Grid(quota, gridWidth, poolHeight, gridHeight, myGrid, numTypes, maxSwaps)
root = Node()
root.state.grid = copy.deepcopy(grid)
finalNode = breadthFirstSearch(root)

solutionPath = getSolutionPath(finalNode)
printSolution(solutionPath)
print(time.clock())





	
