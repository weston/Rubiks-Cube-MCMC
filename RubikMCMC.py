import rubik.rubik as rb
import copy as dc
import random as rand
import numpy as np
import sys

MOVE_SET = ["U","F","R","U'","F'","R'","U2","R2","F2"]
BLOCK_SCORE = 1
MAX_NUM_BLOCKS = 12
NUM_STICKERS = 24
MAX_SCORE = (BLOCK_SCORE * MAX_NUM_BLOCKS) + NUM_STICKERS
#48

#Really dumb function, but oh well
def getNumBlocks(state):
	numBlocks = 0

	#Top layer blocks
	if state[0][0][0] == state[0][2][0] and state[1][0][0] == state[1][0][2]:
		numBlocks += 1
	if state[0][0][0] == state[0][0][2] and state[4][0][0] == state[4][0][2]:
		numBlocks += 1
	if state[0][0][2] == state[0][2][2] and state[3][0][0] == state[3][0][2]:
		numBlocks += 1
	if state[0][2][0] == state[0][2][2] and state[2][0][0] == state[2][0][2]:
		numBlocks += 1

	#Vertical blocks
	if state[1][0][0] == state[1][2][0] and state[4][0][2] == state[4][2][2]:
		numBlocks += 1
	if state[1][0][2] == state[1][2][2] and state[2][0][0] == state[2][2][0]:
		numBlocks += 1
	if state[2][0][2] == state[2][2][2] and state[3][0][0] == state[3][2][0]:
		numBlocks += 1
	if state[3][0][2] == state[3][2][2] and state[4][0][0] == state[4][2][0]:
		numBlocks += 1

	#Bottom Layer blocks
	if state[5][0][0] == state[5][0][2] and state[2][2][0] == state[2][2][2]:
		numBlocks += 1
	if state[5][0][2] == state[5][2][2] and state[3][2][0] == state[3][2][2]:
		numBlocks += 1
	if state[5][2][0] == state[5][2][2] and state[4][2][0] == state[4][2][2]:
		numBlocks += 1
	if state[5][0][0] == state[5][2][0] and state[1][2][0] == state[1][2][2]:
		numBlocks += 1
	return numBlocks

#Takes in a cube object and returns some integer indicating how close it is to being solved.
#Right now this only considers corners to emulate the 2x2 cube
#Extremely rudamentary implementation of this right now
def scoreCubeState(cubeState):
	score = 0
	state = cubeState.cube
	for face in range(6):
		if state[face][0][0] == face:
			score += 1
		if state[face][0][2] == face:
		 	score += 1
		if state[face][2][0] == face:
		 	score += 1
		if state[face][2][2] == face:
			score += 1
	score += BLOCK_SCORE * getNumBlocks(state)
	return score

#Takes in a cube object and returns true if the corners are soved. Returns false otherwise.
def isSolved(cubeState):
	state = cubeState.cube
	for face in range(6):
		if state[face][0][0] != face or state[face][0][2] != face or state[face][2][0] != face or state[face][2][2] != face:
			return False
	return True

def trimMoveString(mv):
	moveArr = str(mv).split()
	suffixes = [" ","2","'"]
	changedSomething = True
	while changedSomething == True:
		changedSomething = False
		for i in range(len(moveArr) - 1):
			if moveArr[i][0] == moveArr[i+1][0]:
				total = 0
				firstMove = list(moveArr[i])
				secondMove = list(moveArr[i + 1])
				changedSomething = True
				if len(firstMove) == 1:
					total += 1
				if len(firstMove) > 1 and firstMove[1] == '2':
					total += 2
				if len(firstMove) > 1 and firstMove[1] == "'":
					total += 3
				if len(secondMove) == 1:
					total += 1
				if len(secondMove) > 1 and secondMove [1] == '2':
					total += 2
				if len(secondMove) > 1 and secondMove [1] == "'":
					total += 3
				moveArr.pop(i + 1)
				total = total % 4
				if len(firstMove) == 1:
					firstMove.append(" ")
				if total == 0:
					moveArr.pop(i)
					break
				if total == 1:
					firstMove[1] = ""
				if total == 2:
					firstMove[1] = "2"
				if total == 3:
					firstMove[1] = "'"
				moveArr[i] = "".join(firstMove)
				break
	return " ".join(moveArr)



#Takes in a move string and randomly changes one move in the string
def alterSolution(scramble):
	scrambleArr = dc.deepcopy(scramble).split()
	scrambleLength = len(scrambleArr)
	numChanges = rand.randint(1,17)
	for i in range(numChanges):
		newMoveIndex = rand.randint(0,len(MOVE_SET) - 1)
		oldMoveIndex = rand.randint(0,scrambleLength - 1)
		scrambleArr[oldMoveIndex] = MOVE_SET[newMoveIndex]
	return " ".join(scrambleArr)

#Generates a random string of moves as a candidate solution
def genRandomSolution():
	solutionLength = rand.randrange(13, 18)
	moveSetLen = len(MOVE_SET)
	solution = ""
	for i in range(solutionLength):
		moveIndex = rand.randint(0,moveSetLen - 1)
		solution += MOVE_SET[moveIndex] + " "
	return solution

#Main function runs the main MCMC routines
def main():
	c = rb.Cube()
	alg = rb.Algorithm(genRandomSolution())
	#alg = rb.Algorithm(sys.argv[1])
	c.apply_alg(alg)
	candidateSolution = genRandomSolution()
	candidateSolutionCube = dc.deepcopy(c)
	candidateSolutionCube.apply_alg(rb.Algorithm(candidateSolution))
	candidateScore = scoreCubeState(candidateSolutionCube)###
	bestSolution = candidateSolution
	bestScore = candidateScore
	T = 10000
	print "Beginning the search for a solution to",
	print trimMoveString(alg)
	numIters = 0
	while bestScore < MAX_SCORE:
		numIters += 1
		if (numIters % 1000 == 0):
			print " .",
		if numIters % 10000 == 0:
			print "Considered " + str(numIters) + " solutions so far. " + str(bestScore) +"/" + str(MAX_SCORE)
			print "Searching . . .",
		newSolution = alterSolution(candidateSolution)
		newCube = dc.deepcopy(c)
		newCube.apply_alg(rb.Algorithm(newSolution))
		newScore = scoreCubeState(newCube)
		d = candidateScore - newScore
		prob = np.e**(-d/ T)
		if d < 0 or rand.random() <= prob:
			candidateScore = newScore	
			candidateSolution = newSolution
		if candidateScore > bestScore:
			bestSolution = candidateSolution
			bestScore = newScore
	print trimMoveString(alg)
	print "The solution to the scramble ",  
	print trimMoveString(alg), 
	print " is: " 		
	print trimMoveString(bestSolution)
	print "Considered " + str(numIters) + " solutions."


main()