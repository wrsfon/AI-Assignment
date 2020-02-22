import numpy as np

def probNgoal(n):
  prob = np.random.random_integers(1, 9, (n,n))
  goalState = np.random.random_integers(1, 2**n-1, n)
  goalPosotion = np.asarray([list(map(int, bin(x)[2:].zfill(5))) for x in goalState])

  goalSum = [list(prob[i] * goalPosotion[i]) for i in range(5)]
  sumX = np.sum(goalSum, axis=0)
  sumY = np.sum(goalSum, axis=1)
  return prob, goalState, goalPosotion, goalSum, sumX, sumY

prob, goalState, goalPosotion, goalSum, sumX, sumY = probNgoal(5)
print("problem: \n", prob)
print("goal state: \n", goalState)
print("goal position: \n", goalPosotion)
print("goal sum: \n", goalSum)
print("sum x: \n", sumX)
print("sum y: \n", sumY)