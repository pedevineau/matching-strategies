from hungarian_algorithm import algorithm

# possible destinations are Olympe (O), Tartare (T), Valhalla (V), Carnutes (C), Gizeh (G) and Paris (P)

# every one must have the same number of choices. In this example every one has three choices. The first counts for 3, the second for 2 and the third for 1
# every possible desination must appear at least in the choice list, at least with the weight 0. Thus the algorithm knows all the possibilities

G = {
	'Amon': {'G': 3, 'P': 2, 'V': 1},
	'Baal': {'G': 3, 'O': 2, 'P': 1},
	'Ceres': {'O': 3, 'C': 2, 'V': 1},
	'Diane': {'O': 3, 'G': 2, 'P': 1},
	'Esus': {'C': 3, 'V': 2, 'P': 1},
    'Freyja': {'V':3, 'P':2, 'O': 1, 'T':0}
}




solution = algorithm.find_matching(G, matching_type = 'max', return_type = 'list')

print(solution)
