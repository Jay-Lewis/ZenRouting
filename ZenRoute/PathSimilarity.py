__author__ = 'Justin'


def pathSimilarity(pathA,pathB):
    num_same_nodes = 0
    for node in pathA:
        if node in pathB:
            num_same_nodes += 1
    percentage = num_same_nodes/max(len(pathA),len(pathB))
    return percentage