# Rubik's Cube MCMC
Markov Chain Monte Carlo Solver for a 2x2 Rubik's Cube

The algorithm:
	For a given scramble
	Choose a random N length string of moves as a candidate solution
	while the candidate solution does not actually solve the scramble
		-Score the candidate solution
		-Change one move of the candidate solution to get a new candidate solution
		-If this new solution is better than the candidate solution, update the candidate solution to be the new solution.
		-Else, with probability e^(-d/t), update the candidate solution to the new solution, where d is the difference in scores between the candidate solution and the new solution, and t is some constant > 0 that governs the trade off between local search and random search.

#Pseudocode:

	state = current_state()
	candidate_solution = random_moves(N)
	best = candodate_solution
	while !is_valid_solution(candidate_solution,state)
		new_candidate = change_one_move_randomly(solution)
		d = score(new_candidate) - score(candidate_solution)
		if d < 0 OR random() < e^(-d/t)
			candidate_solution = new_candidate
		if score(candidate_solution) < score(best)
			best = candidate_solution

	return candidate_solution



#*Scoring a state:
As of now, the scoring algorithm is: #correctStickers + (blockWeight * #blocks)
It seems to perform well for blockWeight = ~4. This hueristic has the problem that a two-swap, on a 2x2 cube, is many moves from being solved, but has a very good score in this hueristic.


Eventually I'll make this in C++ for a 3x3, but for now I'll make it in python for a 2x2 to see if it has any promise. For this I'll be using David Adams's rubik python library. https://github.com/alotofdavid/rubik

#How to run:
In the project directory, invoke "Python RubikMCMC.py"

It will generate a scramble for it to solve, and then begin searching for a solution.

#Example solutons found by RubikMCMC.py 
4/29/2015
Given pretty short scrambles for now...

F R U F R F' -> U' R2 F' U2 R' U2 R

U R U F U R U' R2 -> R2 U F' R' U' F' U2
