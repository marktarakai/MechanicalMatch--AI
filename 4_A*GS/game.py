# Mark Tarakai
# CS5400: Introduction to Artificial Intelligence -- Section 1A
# Puzzle Assignment Series: Mechanical Match -- Segment IV
# A*GS Implementation

# Necessary libraries
from copy import deepcopy
from queue import PriorityQueue
import time
import sys

# Read in the puzzle file to instantiate the puzzle. The puzzle file is
# specified on the command line and the argument is parsed below.
# NEW FEATURE: As requested by the TAs, correct format is handled, and lack
# of parameter is handled. This can handle any file of type 'puzzle*.txt' and
# will produce the associated 'solution*.txt'
try:
    sys.argv[1]
except:
    print("Execution Failure:")
    print("No parameter detected. Retry with correct file as parameter.")
    quit()

exec_param = sys.argv[1]
if exec_param[0:6] != "puzzle":
    print("Execution Failure:")
    print("Please use specified files from problem prompt: 'puzzle*.txt'.")
    quit()
if exec_param[7:11] != ".txt":
    print("Execution Failure:")
    print("Incorrect format. Please retry with specified 'puzzle*.txt' files.")
    quit()
else:
    file = open(exec_param,'r')

# This function creates the puzzle object, and reads in the correct pieces from
# the problem prompt. It reads in everything as ints, and iteratively places the
# pieces into the puzzle. Whitespace is stripped.
class Puzzle:
    quota = int(file.readline())
    maxSwaps = int(file.readline())
    deviceTypes = int(file.readline())
    gridWidth = int(file.readline())
    gridHeight = int(file.readline())
    poolHeight = int(file.readline())
    bonusRules = file.readline()
    grid = []
    # Push the puzzle into a 2D array
    for i in range(gridHeight):
        grid.append([0 for i in range(gridWidth)])

    for i in range(gridHeight):
        line = file.readline()
        line = "".join(line.split())
        for j, num in enumerate(line):
            grid[i][j] = int(num)

# Create state object, constructor takes parameters from a puzzle class object,
# score is placed here.
class State:
    def __init__(self, grid, gridWidth, gridHeight, poolHeight,
        deviceTypes, score = 0):
        self.grid = deepcopy(grid)
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.poolHeight = poolHeight
        self.deviceTypes = deviceTypes
        self.score = score

# Create node object for A*GS with all the criteria from both the professor
# and textbook. Constructor sets them initially to none-type, with a 0 pathcost
# The less-than operator is overloaded, to allow easy comparison of f(n) values
# The function value has been added.
# The __lt__ method has been defined to overload the < operator for
# priority queue prioritization. The function value is comparative criteria.
class Node:
    def __init__(self, State = None, Parent = None, Action = None,
        pathCost = 0, fn = 0):
        self.State = State
        self.Parent = Parent
        self.Action = Action
        self.pathCost = pathCost
        self.fn = fn

    def __lt__(self, compare_node):
        return (self.fn < compare_node.fn)

# This function finds a matching row, so if a row/col has three or more,
# the function places the coordinates of those in a list, which is
# passed to a function to make 0.
def findMatches(grid, gridWidth, gridHeight, poolHeight):
    makeVacant = []
    for i in range(poolHeight, gridHeight):
        sameCheck = 0
        matchQuant = 0
        for j in range(gridWidth):
            if j == 0:
                sameCheck = grid[i][j]
            else:
                if sameCheck == grid[i][j]:
                    matchQuant = matchQuant + 1
                    if matchQuant >= 2 and j == gridWidth - 1:
                        for n in range(matchQuant + 1):
                            makeVacant.append((i, j-n))
                else:
                    if matchQuant < 2:
                        sameCheck = grid[i][j]
                        matchQuant = 0
                    else:
                        for n in range(matchQuant +1):
                            makeVacant.append((i, j-1-n))
                        sameCheck = grid[i][j]
                        matchQuant = 0
    # check the columns for matches
    for j in range(gridWidth):
        sameCheck = 0
        matchQuant = 0
        for i in range(poolHeight, gridHeight):
            if i == 0:
                sameCheck = grid[i][j]
            else:
                if sameCheck == grid[i][j]:
                    matchQuant = matchQuant + 1
                    if matchQuant >= 2 and i == gridHeight - 1:
                        for n in range(matchQuant + 1):
                            makeVacant.append((i-n,j))
                elif sameCheck != grid[i][j]:
                    if matchQuant < 2:
                        sameCheck = grid[i][j]
                        matchQuant = 0
                    else:
                        for n in range(matchQuant + 1):
                            makeVacant.append((i-1-n,j))
                        sameCheck = grid[i][j]
                        matchQuant = 0
    return makeVacant

# This function makes the list of needed vacancies, vacant.
def Vacantize(makeVacant, grid):
    for i in makeVacant:
        grid[i[0]][i[1]] = 0

# This function fills the board vacancies, it handles the cascading effect
# desired by the instructor, and gets a new device.
def fillBoard(deviceTypes, grid, gridWidth, gridHeight, poolHeight):
    numReplaced = 0
    for i in range(poolHeight, gridHeight):
        for j in range(gridWidth):
            if grid[i][j] == 0:
                for x in range(i):
                    grid[i-x][j] = grid[i-x-1][j]
                numReplaced = numReplaced + 1
                grid[0][j] = makeNewDevice(grid,deviceTypes,j,numReplaced)

# This function fabricates a new device to place on the board, as asked by the
# fill board function. It uses the formula given in the Puzzle Assignment
# Series prompt.
def makeNewDevice(grid, deviceTypes, j, numReplaced):
    deviceType = grid[1][j]
    newDevice = ((int(deviceType)+j+numReplaced)%deviceTypes)+1
    return newDevice

# This function is not needed for any type of purpose, but allows the user
# to print a well-formatted grid if needed. Particularly useful if code is
# to be tested in Python IDLE.
def gridPrint(grid):
    for row in grid:
        print(*row)

# Look operations, these four functions return the device value in the direction
# specified. This methodology was adapted to avoid full board scans for every
# swap.
def lookUp(grid, i, j, poolHeight):
    if i-1 >= poolHeight:
        return grid[i-1][j]
    else:
        return 0

def lookDown(grid, i, j, gridHeight):
    if i+1 < gridHeight:
        return grid[i+1][j]
    else:
        return 0

def lookRight(grid, i, j, gridWidth):
    if j+1 < gridWidth:
        return grid[i][j+1]
    else:
        return 0

def lookLeft(grid, i, j):
    if j-1 > 0:
        return grid[i][j-1]
    else:
        return 0

'''
This is the possible actions function specified by the textbook and professor.
The logic is extremely difficult to derive from the code, due to the nature
of the traversals, but will be broken down here. The two scan directions are
vertical and horizontal, and they are individual processes in the function.
For both, the function appends the first element in the grid to a list. Then
it is compared to the next one, if this matches, it continues. If this does not
match, it looks down and looks up to see if a middle swap is possible. If this
is not possible it moves. An identical process occurs for the vertical swaps.
It then returns a set of tuples of two coordinates (in one tuple). These are
the possible swaps for the given state, a parameter in the function call.
'''
def Actions(s):
    possibleActions = set()
    for i in range(s.poolHeight, s.gridHeight):
        tempMatch = []
        size_match = len(tempMatch)
        for j in range(s.gridWidth):
            if j == 0:
                tempMatch.append(s.grid[i][j])
            else:
                if s.grid[i][j] == tempMatch[0]:
                    tempMatch.append(s.grid[i][j])
                    if j == s.gridWidth-1:
                        if len(tempMatch) > 1:
                            if lookUp(s.grid,i,j-2,
                                s.poolHeight) == tempMatch[0]:
                                if(i-1,j-2,i,j-2) not in possibleActions:
                                    possibleActions.add((i,j-2,i-1,j-2))
                            if lookLeft(s.grid,i,j-2) == tempMatch[0]:
                                if(i,j-3,i,j-2) not in possibleActions:
                                    possibleActions.add((i,j-2,i,j-3))
                            if lookDown(s.grid,i,j-2,
                                s.gridHeight) == tempMatch[0]:
                                if(i-1,j-2,i,j-2) not in possibleActions:
                                    possibleActions.add((i,j-2,i-1,j-2))
                else:
                    if len(tempMatch) > 1:
                        # right of match sequence
                        if lookUp(s.grid, i, j, s.poolHeight) == tempMatch[0]:
                            if (i-1,j,i,j) not in possibleActions:
                                possibleActions.add((i,j,i-1,j))
                        if lookRight(s.grid, i, j, s.gridWidth) == tempMatch[0]:
                            if (i,j+1,i,j) not in possibleActions:
                                possibleActions.add((i,j,i,j+1))
                        if lookDown(s.grid, i, j, s.gridHeight) == tempMatch[0]:
                            if (i+1,j,i,j) not in possibleActions:
                                possibleActions.add((i,j,i+1,j))
                        # left of match sequence
                        if j-(len(tempMatch)+1) >= 0:
                            if lookUp(s.grid, i, j-(len(tempMatch)+1),
                                s.poolHeight) == tempMatch[0]:
                                if (i-1,j-(len(tempMatch)+1),i,
                                    j-(len(tempMatch)+1)) not in possibleActions:
                                    possibleActions.add((i,j-(len(tempMatch)+1),
                                        i-1,j-(len(tempMatch)+1)))
                            if lookDown(s.grid, i, j-(len(tempMatch)+1),
                                s.gridHeight) == tempMatch[0]:
                                if (i+1,j-(len(tempMatch)+1),i,
                                    j-(len(tempMatch)+1)) not in possibleActions:
                                    possibleActions.add((i,j-(len(tempMatch)+1),
                                        i+1,j-(len(tempMatch)+1)))
                            if lookLeft(s.grid, i,
                                j-(len(tempMatch)+1)) == tempMatch[0]:
                                if (i,j-(len(tempMatch)+2),i,
                                    j-(len(tempMatch)+1)) not in possibleActions:
                                    possibleActions.add((i,j-(len(tempMatch)+1),
                                        i,j-(len(tempMatch)+2)))
                    else:
                        # discover if swapping the middle yields a match
                        if j+1 < s.gridWidth:
                            if s.grid[i][j+1] == tempMatch[0]:
                                if lookUp(s.grid, i, j,
                                    s.poolHeight) == tempMatch[0]:
                                    if (i-1,j,i,j) not in possibleActions:
                                        possibleActions.add((i,j,i-1,j))
                                if lookDown(s.grid, i, j,
                                    s.poolHeight) == tempMatch[0]:
                                    if (i+1,j,i,j) not in possibleActions:
                                        possibleActions.add((i,j,i+1,j))
                    tempMatch = []
                    tempMatch.append(s.grid[i][j])

    for j in range(s.gridWidth):
        tempMatch = []
        for i in range(s.poolHeight,s.gridHeight):
            if i == s.poolHeight:
                tempMatch.append(s.grid[i][j])
            else:
                if s.grid[i][j] == tempMatch[0]:
                    tempMatch.append(s.grid[i][j])
                    if i == s.gridHeight-1:
                        if len(tempMatch) > 1:
                            if lookUp(s.grid,i-2,j,
                                s.poolHeight) == tempMatch[0]:
                                if(i-3,j,i-2,j) not in possibleActions:
                                    possibleActions.add((i-2,j,i-3,j))
                            if lookLeft(s.grid,i-2,j) == tempMatch[0]:
                                if(i-2,j-1,i,j) not in possibleActions:
                                    possibleActions.add((i-2,j,i-2,j-1))
                            if lookRight(s.grid,i-2,j,
                                s.gridWidth) == tempMatch[0]:
                                if(i-2,j+1,i-2,j) not in possibleActions:
                                    possibleActions.add((i-2,j,i-2,j+1))
                else:
                    if len(tempMatch) > 1:
                        # bottom of match sequence
                        if lookLeft(s.grid,i,j) == tempMatch[0]:
                            if(i,j-1,i,j) not in possibleActions:
                                possibleActions.add((i,j,i,j-1))
                        if lookDown(s.grid,i,j,s.gridHeight) == tempMatch[0]:
                            if(i+1,j,i,j) not in possibleActions:
                                possibleActions.add((i,j,i+1,j))
                        if lookRight(s.grid,i,j,s.gridWidth) == tempMatch[0]:
                            if(i,j+1,i,j) not in possibleActions:
                                possibleActions.add((i,j,i,j+1))
                        # top of match sequence
                        if i-(len(tempMatch)+1) >= s.poolHeight:
                            if lookLeft(s.grid, i-(len(tempMatch)+1),
                                j) == tempMatch[0]:
                                if (i-(len(tempMatch)+1),j-1,
                                    i-(len(tempMatch)+1),
                                    j) not in possibleActions:
                                    possibleActions.add((i-(len(tempMatch)+1),
                                        j,i-(len(tempMatch)+1),j-1))
                            if lookUp(s.grid,i-(len(tempMatch)+1),j,s.poolHeight) == tempMatch[0]:
                                if(i-(len(tempMatch)+2),j,i-(len(tempMatch)+1),j) not in possibleActions:
                                    possibleActions.add((i-(len(tempMatch)+1),j,i-(len(tempMatch)+2),j))
                            if lookRight(s.grid,i-(len(tempMatch)+1),j,s.gridWidth) == tempMatch[0]:
                                if (i-(len(tempMatch)+1),j+1,i-(len(tempMatch)+1),j) not in possibleActions:
                                    possibleActions.add((i-(len(tempMatch)+1),j,i-(len(tempMatch)+1),j+1))
                    else:
                        # discover if swapping the middle yields a match
                        if i+1 < s.gridHeight:
                            if s.grid[i+1][j] == tempMatch[0]:
                                if lookLeft(s.grid,i,j) == tempMatch[0]:
                                    if(i,j-1,i,j) not in possibleActions:
                                        possibleActions.add((i,j,i,j-1))
                                if lookRight(s.grid,i,j,
                                    s.gridWidth) == tempMatch[0]:
                                    if(i,j+1,i,j) not in possibleActions:
                                        possibleActions.add((i,j,i,j+1))
                    tempMatch = []
                    tempMatch.append(s.grid[i][j])
    return possibleActions

# This function performs the actual swap. It takes the action and state to
# perform the operation to a grid by reference
def swap(s,a):
    i_to = a[0]
    j_to = a[1]
    i_from = a[2]
    j_from = a[3]
    temp = s.grid[i_from][j_from]
    s.grid[i_from][j_from] = s.grid[i_to][j_to]
    s.grid[i_to][j_to] = temp

# This functions stabilizes the board. It continues to fill and match until the
# match location list is empty. No matches remain if this is reached.
def stabilizeBoard(s):
    match_loc = findMatches(s.grid,s.gridWidth,s.gridHeight,s.poolHeight)
    while match_loc:
        for loc in match_loc:
            s.score = s.score + 1
        Vacantize(match_loc,s.grid)
        fillBoard(s.deviceTypes, s.grid, s.gridWidth, s.gridHeight,
         s.poolHeight)
        match_loc = findMatches(s.grid,s.gridWidth,s.gridHeight,s.poolHeight)

# This function is the TRANSITION MODEL, it takes a state and action and returns a
# new state based on those two parameters. It performs the necessary operations,
# and "brings together" the rest of the program, by performing the action,
# stabilizing the board and returning a new state with this information
def Result(s,a):
    newState = State(s.grid,s.gridWidth,s.gridHeight,s.poolHeight,
        s.deviceTypes,s.score)
    swap(newState,a)
    stabilizeBoard(newState)
    return newState

# This function creates child-nodes. It creates an Node object based on state
# of parent, path-cost, and action and returns it for use in the pertinent
# algorithm
def ChildNode(parent,a):
    childNode = Node(Result(parent.State, a), parent, a,
            parent.pathCost + 1)
    return childNode

# This solves the puzzle and appends the parent nodes to a solution list
# to follow the traversal of the tree. It continues while the parent does
# not exist.
def Solve(node):
    solution = []
    while node.Parent != None:
        solution.append(node.Action)
        node = node.Parent
    return solution

# The following three functions scan for identical characteristics in the nodes
# and makes sure the same one is not added to either the frontier or the
# explored set. These checks are implemented in the driver function for
# A*GS.
def CheckFrontier(state, frontier):
    for iter_node in frontier.queue:
        node = iter_node[1]
        if state.score == node.State.score and state.grid == node.State.grid:
            return True
        else:
            return False

def CheckExplored(state, explored):
    for node in explored:
        if state.score == node.score and state.grid == node.grid:
            return True
        else:
            return False

# This function checks path-cost and returns it the search algorithm to assist
# in the decision to replace the existing node with the incoming node, this
# decision is based on cheaper path-cost.
def CheckCost(node, frontier):
    for iter_node in frontier.queue:
        exist_node = iter_node[1]
        if exist_node.pathCost > node.pathCost:
            return True
        else:
            return False

# Here is my implementation of A*GS. The algorithm follows the exact specification 
# in the text of a general graph search, with an added heuristic check. The 
# heuristic h(n) = puzzle_quota - current_score.
# Additional functions, described and defined above are implemented to clean up
# the checking sequence.
# A priority queue is imported from the Python3 included libraries. The __lt__
# method is defined to overload the operator is allow direct object comparison
# with the evaluation function value f(n) as the criteria.
def A_star_GS(puzzle):
    explored = set()
    frontier = PriorityQueue()
    init_state = State(newPuzzle.grid,newPuzzle.gridWidth,newPuzzle.gridHeight,
                       newPuzzle.poolHeight,newPuzzle.deviceTypes,0)
    init_node = Node(init_state)
    gn = newPuzzle.maxSwaps*init_node.pathCost
    hn = newPuzzle.quota-init_node.State.score
    init_node.fn = gn+hn
    frontier.put((init_node.fn,init_node))
    while frontier != []:
        temp_node = frontier.get()
        leaf = temp_node[1]
        if leaf.pathCost > newPuzzle.maxSwaps:
            return []
        elif leaf.State.score >= puzzle.quota:
            sol = Solve(leaf)
            return sol
        explored.add(leaf.State)
        action_set = Actions(leaf.State)
        for action in action_set:
            child = ChildNode(leaf,action)
            hn = newPuzzle.quota-child.State.score
            gn = newPuzzle.maxSwaps*child.pathCost
            child.fn = gn+hn
            if not CheckFrontier(child.State,frontier) and not CheckExplored(child.State,explored):
                frontier.put((child.fn,child))
            if CheckFrontier(child.State,frontier) and CheckCost(child,frontier):
                frontier.put((child.fn,child))
'''
This function takes the solution, the puzzle, and the time taken and prints it
out to a text file 'solution*.txt'. This assumes the file follows the
'puzzle*.txt' format and will create a solution*.txt output file based on the
input file. It also writes execution time and is formatted exactly to course
regulations.
'''
def printOut(Puzzle, Solution, TimeTaken):
    file_name = "solution"+exec_param[6]+".txt"
    solfile = open(file_name, 'w')
    quota = str(Puzzle.quota) + "\n"
    maxSwaps = str(Puzzle.maxSwaps)+"\n"
    devicetypes = str(Puzzle.deviceTypes)+"\n"
    gridWidth = str(Puzzle.gridWidth)+"\n"
    gridHeight = str(Puzzle.gridHeight)+"\n"
    poolHeight = str(Puzzle.poolHeight)+"\n"
    bonusRules = str(Puzzle.bonusRules)
    solfile.write(quota)
    solfile.write(maxSwaps)
    solfile.write(devicetypes)
    solfile.write(gridWidth)
    solfile.write(gridHeight)
    solfile.write(poolHeight)
    solfile.write(bonusRules)

    for Row in Puzzle.grid:
        for num in Row:
            PrintNum = str(num)+" "
            solfile.write(PrintNum)
        solfile.write("\n")
    if solution == []:
        solfile.write("No Solution")
    else:
        for swap in reversed(solution):
            solfile.write("({},{}),({},{})\n".format(swap[1],swap[0],
                swap[3],swap[2]))
    TimeTaken = str(TimeTaken)
    solfile.write(TimeTaken)
    solfile.close()

newPuzzle = Puzzle()
start = time.clock()
solution = A_star_GS(newPuzzle)
total = (time.clock() - start)
printOut(newPuzzle, solution, total)
file.close()