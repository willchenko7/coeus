'''
Goal: Convert dictionary of various formulas to a hypergraph that connects the formulas to the variables they use.

This can be used to represent a graph connecting all formulas and is used to find the shortest path between the desired variable and the known variables.

Input:
    - {'eq0': 'miles_per_hour=60', 'eq1': 'time_in_hours=2', 'eq2': 'distance_travelled=miles_per_hour*time_in_hours'}

Output:
    - {
        'eq0': ['miles_per_hour'], 
        'eq1': ['time_in_hours'], 
        'eq2': ['distance_travelled', 'miles_per_hour', 'time_in_hours']
    }
'''
import re

def formulaDictionary2Hypergraph(formula_dictionary):
    #list of symbols that are NOT variables but are included in the formulas
    symbols_not_included = ['sin','cos','tan','sqrt']
    formula_hypergraph = {}
    for eq_name,formula in formula_dictionary.items():
        #get all unique variables in the formula
        unique_vars = sorted(list(set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', formula))))
        #remove any symbols that are not variables
        unique_vars = [i for i in unique_vars if i not in symbols_not_included]
        #add the formula to the hypergraph
        formula_hypergraph[eq_name] = unique_vars
    return formula_hypergraph


if __name__ == '__main__':
    formula_dictionary = {'eq0': 'miles_per_hour=60', 'eq1': 'time_in_hours=2', 'eq2': 'distance_travelled=miles_per_hour*time_in_hours'}
    formula_hypergraph = formulaDictionary2Hypergraph(formula_dictionary)
    print(formula_hypergraph)
