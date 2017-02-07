__author__ = 'Pablo'

# DESCRIPTION:
# This script takes a dictionary ("edge_dictionary"), keys of interest, and a list ("weights") as inputs. It then generates
# a weighted sum of the values of interest.
#

def weightfunction(weights,edge_dictionary,keys):

    values=[]    #empty values list

    for key in keys:         #append the values from dictionary into the 'values' list
        values.append(edge_dictionary[key])

    mult_lists = [a * b for a, b in zip(weights, values)]       #multiply both lists
    total = sum(i for i in mult_lists)       #add lists
    return total