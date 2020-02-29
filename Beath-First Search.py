# Breadth-first search
import numpy as np
# goal state: [ 4  6 19  1 21]
goalState = np.array([3,4,14,13])
startState = np.zeros((1,4), dtype=np.int)
print(goalState, startState)

def isSameState(state1: np, state2: np):
    return (state1 == state2).all()

def formatState(state: np):
    arraySize = state.shape[1] * (-1)
    indexChecker = -1
    formatState = state
    while(indexChecker > arraySize): 
        if formatState[0, indexChecker] == 16:
            formatState[0, indexChecker] = 0
            formatState[0, indexChecker-1] += 1
        indexChecker -= 1
    return formatState

def doBreadthFirstSearch(startState: np, goalState: np):
    if startState.shape[1] != goalState.shape[0]:
        print("! Error input: StartState size mismatch with GoalState!")
        return
    arraySize = goalState.shape[0]
    currentState = startState
    while not isSameState(currentState, goalState):
        currentState[0, -1] += 1
        currentState = formatState(currentState)
        print(currentState.tolist()[0])
    return currentState

    # Recursive way -> Not good
    # if isSameState(startState, goalState):
    #     return startState
    # else:
    #     currentState = startState
    #     currentState[0, -1] += 1
    #     currentState = formatState(currentState)
    #     currentState = doBreadthFirstSearch(currentState, goalState)
    #     return currentState
    # Current State +1 at the last of index
    


# Main ###############################################
print(doBreadthFirstSearch(startState, goalState))
