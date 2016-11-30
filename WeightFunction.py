__author__ = 'Pablo'

"""
The function takes a dictionary ("edge_dictionary") and a list ("weights") as inputs. It then appends the desired values
from the dictionary into a list ("values") and multiplies and adds it with the "weights" list to get a "zen score"
"""

def zen_score(weights,edge_dictionary):
    keys = ['traffic','time','distance']   #define the keys to be looked for in the dictionary
    values=[]    #empty values list

    for key in keys:         #append the values from dictionary into the 'values' list
        values.append(edge_dictionary[key])

    mult_lists = [a * b for a, b in zip(weights, values)]       #multiply both lists
    total = sum(i for i in mult_lists)       #add lists
    return total