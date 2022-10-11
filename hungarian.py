"""
The Hungarian algorithm is based on bicliques. 
It assumes the choice is asymetric: there is a group of candidates on one hand, and a group of chosen entities on the other.
If your problem assumes that both sides rank the other side, or if it assumes there is no "2 groups" at all,
the Hungarian algorithm is not adapted. Then see respectively the Stable Marriage problem (e.g Shapley-Gale algo) and the Maximum cardinality matching problem (e.g blossom algoritm)

In this example, Ancient Gods search for a resting place to rule forever. Every god must have a resting place, and every place must have a ruler.
In our vanilla example, the possible destinations are Olympe (O), Tartare (T), Valhalla (V), Carnutes (C), Gizeh (G) and Paris (P).

Some places are more attractive than other, it is why must sort their n preferred places (here n=3). The first counts for 3 point, the second for 2 point and the third for 1 point.
The algorithm maximizes the affectation in a way that maximize the sum of points associated with the ranking the god made.

IMPORTANT: Every possible destination must appear at least once in the choice list, possibly with a null weight. 
Thus the algorithm will know all the possible places and it grants that every place will find someone.

"""

from hungarian_algorithm import algorithm

possible_dest = set(["O", "T", "V", "C", "G", "P"])
whishes = {
	'Amon': {'G': 3, 'P': 2, 'V': 1},
	'Baal': {'G': 3, 'O': 2, 'P': 1},
	'Ceres': {'O': 3, 'C': 2, 'V': 1},
	'Diane': {'O': 3, 'G': 2, 'P': 1},
	'Esus': {'C': 3, 'V': 2, 'P': 1},
    'Freyja': {'V':3, 'P':2, 'O': 1}
}

# Let us complete the whishes matrix to ensure that all possible destinations appear (possibly with weight 0)
ranked_dest = set([p for god, choices in whishes.items() for p in choices.keys()])

if len(ranked_dest.union(possible_dest)) < len(whishes.keys()):
	raise Exception("The algorithm has no solution if the number of possible places < the number of candidates")

if (possible_dest ^ ranked_dest):
    if (ranked_dest - possible_dest):
        print(f"Be aware that some places that appear in your choices are not mentioned in your 'possible_choices': {ranked_dest-possible_dest}")
    if (possible_dest - ranked_dest):
        one_god = list(whishes.keys())[0]
		# Add the places that no one ranked at a random candidate with a null weight (the identity of the candidate has no impact)
        for dest in (possible_dest - ranked_dest):
            whishes[one_god][dest] = 0

# Be aware the library have no solution
hungarian_solution = algorithm.find_matching(whishes, matching_type = 'max', return_type = 'list')

points = sum([pt for (affectation, pt) in hungarian_solution])
print(f"Total points of the proposed affectations: {points}")
print(hungarian_solution)
