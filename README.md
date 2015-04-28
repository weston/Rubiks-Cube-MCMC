# Rubik's Cube MCCS
Markov Chain Monte Carlo Solver for a 2x2 Rubik's Cube

The algorithm:
	For a given scramble
	Choose a random N length string of moves as a candidate solution
	while the candidate solution does not actually solve the scramble
		-Score the candidate solution
		-Change one move of the candidate solution to get a new candidate solution
		-If this new solution is better than the candidate solution, update the candidate solution to be the new solution.
		-Else, with probability e^(-d/t), update the candidate solution to the new solution, where d is the difference in scores between the candidate solution and the new solution, and t is some constant > 0 that governs the trade off between local search and random search.

Pseudocode:

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



*Scoring a state:
	For now, a state's score should be a function of how many pieces are solved, and but also how many pieces are solved with respect to adjacent pieces.