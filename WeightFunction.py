def zen_score(weights,edge_dictinonary):      
    keys = ['traffic','time','distance']
    values=[]
    
    for key in keys:
        values.append(edge_dictionary[key])
        
    mult_lists = [a * b for a, b in zip(weights, values)]       #Multiply both lists
    total = sum(i for i in mult_lists)       #Add lists
    return total

"""TEST

list_weight = [1, 2, 3]
list_values = [1, 3, 3]
result = zen_score(list_weight, list_values)

print "The weight is: ", result

"""
