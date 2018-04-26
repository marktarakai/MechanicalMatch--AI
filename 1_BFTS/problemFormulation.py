# Mark Tarakai

# This Python module represents the problem formulation and contains all
# pertinent components laid out in the lecture and textbook that represent
# a "well-defined problem".

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
    index = len(tempMatch)
    for i in range(s.poolHeight, s.gridHeight):
        tempMatch = []
        size_match = index
        for j in range(s.gridWidth):
            if j == 0:
                tempMatch.append(s.grid[i][j])
            else:
                if s.grid[i][j] == tempMatch[0]:
                    tempMatch.append(s.grid[i][j])
                    if j == s.gridWidth-1:
                        if index > 1:
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
                    if index > 1:
                        # right of match sequence
                        if lookUp(s.grid, i, j, s.poolHeight) == tempMatch[0]:
                            if (i-1,j,i,j) not in possibleActions:
                                possibleActions.add((i,j,i-1,j))
                        if lookRight(s.grid,i,j,s.gridWidth) == tempMatch[0]:
                            if (i,j+1,i,j) not in possibleActions:
                                possibleActions.add((i,j,i,j+1))
                        if lookDown(s.grid, i, j, s.gridHeight) == tempMatch[0]:
                            if (i+1,j,i,j) not in possibleActions:
                                possibleActions.add((i,j,i+1,j))
                        # left of match sequence
                        if j-(index+1) >= 0:
                            if lookUp(s.grid, i, j-(index+1), 
                                s.poolHeight) == tempMatch[0]:
                                if (i-1,j-(index+1),i,
                                    j-(index+1)) not in possibleActions:
                                    possibleActions.add((i,j-(index+1),
                                        i-1,j-(index+1)))
                            if lookDown(s.grid, i, j-(index+1), 
                                s.gridHeight) == tempMatch[0]:
                                if (i+1,j-(index+1),i,
                                    j-(index+1)) not in possibleActions:
                                    possibleActions.add((i,j-(index+1),
                                        i+1,j-(index+1)))
                            if lookLeft(s.grid, i, 
                                j-(index+1)) == tempMatch[0]:
                                if (i,j-(index+2),i,
                                    j-(index+1)) not in possibleActions:
                                    possibleActions.add((i,j-(index+1),
                                        i,j-(index+2)))
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
                        if index > 1:
                            if lookUp(s.grid,i-2,j,
                                s.poolHeight) == tempMatch[0]:
                                if(i-3,j,i-2,j) not in possibleActions:
                                    possibleActions.add((i-2,j,i-3,j))
                            if lookLeft(s.grid,i-2,j) == tempMatch[0]:
                                if(i-2,j-1,i,j) not in possibleActions:
                                    possibleActions.add((i-2,j,i-2,j-1))
                            if lookRight(s.grid,i-2,j,
                                s.gridHeight) == tempMatch[0]:
                                if(i-2,j+1,i-2,j) not in possibleActions:
                                    possibleActions.add((i-2,j,i-2,j+1))
                else:
                    if index > 1:
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
                        if i-(index+1) >= s.poolHeight:
                            if lookLeft(s.grid, i-(index+1), 
                                j) == tempMatch[0]:
                                if (i-(index+1),j-1,
                                    i-(index+1),
                                    j) not in possibleActions:
                                    possibleActions.add((i-(index+1),
                                        j,i-(index+1),j-1))
                            if lookUp(s.grid,i-(index+1),
                                j,s.poolHeight) == tempMatch[0]:
                                if(i-(index+2),j,i-(index+1,
                                    j)) not in possibleActions:
                                    possibleActions.add((i-(index+1),
                                        j,i-(index+2),j))
                            if lookRight(s.grid,i-(index+1),
                                j,s.gridWidth) == tempMatch[0]:
                                if (i-(index+1),j+1,
                                    i-(index+1),
                                    j) not in possibleActions:
                                    possibleActions.add((i-(index+1),j,
                                        i-(index+1),j+1))
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