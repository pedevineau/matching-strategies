"""
The Gale-Shapley algorithm is based on bicliques. It solves the "stable marriage problem". 

It assumes the choice is symmetric: there is a first group of candidates (in the original problem: women wanting to marry men), and a second group of the same size (men wanting to marry women).
Each member of a group ranks all the members of the other group.

The algorithm grants that there is no pair (man, woman) where both participants prefer each other to their matched partners. 

If your problem assumes that only one side rank the other side, see the Hungarian algorithm. 
And if in your problem there is only one group and you want to form pairs in these groups, see the Maximum cardinality matching problem (example of algorithm: the blossom algorithm).

The code below includes both a Python implementation of Gale-Shapley, and an example.
The algorithm grants than all the members of the smaller group will find someone.
"""

from typing import List, Dict, Tuple, Union


def gale_shapley(
    clique1_choices: Dict[str, List[str]],
    clique2_choices: Dict[str, List[str]],
    display_rankings: bool = False,
) -> Union[List[Tuple[str, str, int, int]], List[Tuple[str, str]]]:
    """
    The gale-shapley algorithm input the preferences of each cliques, and return a list of pairs
    granting that there could not be alternative pair (man, woman) where both participants would prefer each other to their matched partners.
    Important: if the dictionaries are not of same size, some are going to remain alone.
    In this function, the smallest dictionary must be clique1. If it is not the case, the function switches clique1 and clique2

    Args:
        clique1_choices (Dict[str, List[int]]): the keys are the names of the clique1 members, and the values are lists of the members of clique2 (ordered from best to worst)
        clique2_choices (Dict[str, List[int]]): the keys are the names of the clique2 members, and the values are lists of the members of clique1 (ordered from best to worst)
        display_rankings: if True, also return for a pair (a, b) the initial ranking (from 0 to n-1) of b in the list of a and the initial ranking (from 0 to n-1) of a in the list of b. Default to False
    Returns:
        List[Tuple[str, str]]: the list of matchings
    """
    if len(clique1_choices) != len(clique2_choices):
        print("The two groups are not of same size. Some would remain alone")
    if len(clique1_choices) > len(clique2_choices):
        print(
            "The input clique1 was longer than the clique2. This is not allowed, hence clique1 and clique2 have been switched"
        )
        clique1_choices, clique2_choices = clique2_choices, clique1_choices

    clique1_not_matched = list(clique1_choices.keys())

    # value of clique1_favourite is the indice in clique1_choices of the preferred person of the key "m" that is still available
    clique1_favourite = {m: 0 for m in clique1_choices.keys()}
    # value of clique2_favourite is the name the preferred person of clique1 that proposed to the key "f" so far
    clique2_suitors = {f: None for f in clique2_choices.keys()}

    while clique1_not_matched:
        # pick a single
        single = clique1_not_matched[-1]
        # this single is proposed to its preferred person in clique2 that is still available
        favourite = clique1_choices[single][clique1_favourite[single]]

        # next time that the "single" will propose (if there is a next time), he will propose to the next in its ranking
        clique1_favourite[single] += 1

        # if this favourite person has no match so far, (temporarily) accept the single
        if clique2_suitors[favourite] is None:
            clique2_suitors[favourite] = single
            clique1_not_matched.remove(single)
        else:
            # there was already a suitor
            previous_suitor = clique2_suitors[favourite]
            # check if the single is preferred to the previous suitor. If he is, the single becomes the new suitor
            if clique2_choices[favourite].index(single) < clique2_choices[
                favourite
            ].index(previous_suitor):
                clique2_suitors[favourite] = single
                clique1_not_matched.remove(single)
                clique1_not_matched.append(previous_suitor)

    # at the end of the loop, every single of clique1 has been matched.
    # There is possibly unmatched member of clique2 if clique2 was longer, then remove the unmatched from the clique2_suitors
    for c in list(clique2_suitors.keys()):
        if clique2_suitors[c] is None:
            clique2_suitors.pop(c)

    if display_rankings:
        pairs = [
            (
                clique1_member,
                clique2_member,
                clique1_choices[clique1_member].index(clique2_member),
                clique2_choices[clique2_member].index(clique1_member),
            )
            for clique2_member, clique1_member in clique2_suitors.items()
        ]
    else:

        pairs = [
            (clique1_member, clique2_member)
            for clique2_member, clique1_member in clique2_suitors.items()
        ]

    return pairs


## The example with schools and candidates

if __name__ == "__main__":

    # The example is based on the French competitive exams for engineering schools
    # Every student must find a position, and esome positions won't be filled due to the lack of candidates
    # in our example, there are two positions at school X and only one position at the others
    exam_rankings = {
        "X_1": ["A", "B", "C", "D"],  # "X exam"
        "X_2": ["A", "B", "C", "D"],  # "X exam"
        "Mines": ["B", "C", "A", "D"],  # Mines
        "ENS": ["B", "A", "C", "D"],  # ENS,
        "Imaginary school": ["A", "C", "D", "B"],
    }

    student_preferences = {
        "A": ["X_1", "X_2", "ENS", "Mines", "Imaginary school"],  # student A
        "B": ["Mines", "X_1", "X_2", "ENS", "Imaginary school"],  # B
        "C": ["Mines", "ENS", "X_1", "X_2", "Imaginary school"],  # C
        "D": ["ENS", "X_1", "X_2", "Mines", "Imaginary school"],  # D
    }

    results = gale_shapley(student_preferences, exam_rankings, display_rankings=True)
    n = len(student_preferences)
    for (student, school, _, rank_at_exam) in results:
        print(
            f"Student {student} will join school {school}, where he was ranked {1+rank_at_exam}/{len(exam_rankings[school])}"
        )
