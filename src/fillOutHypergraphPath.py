
'''

Goal: given a path of nodes in a hypergraph, write out a coeus language question for each step in the path

Inputs:
    - path of nodes in hypergraph
    - formula dictionary
    - variable of interest

Outputs:
    - list of coeus language questions

Example:
    Input:  {'time_in_hours': 'eq1', 'miles_per_hour': 'eq0', 'distance_travelled': 'eq2'}
    Output: ['Solve for distance_travelled: miles_per_hour=60;time_in_hours=2;distance_travelled=miles_per_hour*time_in_hours']
'''

def fillOutHypergraphPath(path,formula_dictionary,var):
    solve_statements = []
    i_path = []
    for v,eq in path.items():
        if v == 'molar_mass_of_chemical':
            ss = f'Solve for molar_mass_of_chemical: chemical={metadata[0]}'
        else:
            ss = f'Solve for {v}: {formula_dictionary[eq]} -->'
        solve_statements.append(ss)
        i_path.append(eq)
        if v == var:
            break
    return solve_statements

if __name__ == '__main__':
    var = 'distance_travelled'
    path = {'time_in_hours': 'eq1', 'miles_per_hour': 'eq0', 'distance_travelled': 'eq2'}
    formula_dictionary = {'eq0': ' miles_per_hour=60', 'eq1': 'time_in_hours=2', 'eq2': 'distance_travelled=miles_per_hour*time_in_hours'}
    solve_statements = fillOutHypergraphPath(path,formula_dictionary,var)
    print(solve_statements)