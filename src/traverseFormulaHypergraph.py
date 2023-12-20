'''

Goal: traverse a given hypergraph and find possible paths between known nodes and unknown nodes

Inputs:
    - hypergraph
    - known nodes

Outputs:
    - possible paths between known nodes and unknown nodes

'''
import re
from getAllTerms import getAllTerms
from formulaDictionary2Hypergraph import formulaDictionary2Hypergraph
from formulas2Dictionary import formulas2Dictionary

def get_edges(formula_hypergraph,voi):
    '''
    get edges in hypergraph for variable of interest (voi) by getting eqs containg voi
    '''
    edges = []
    for k,v in formula_hypergraph.items():
        if voi in v:
            edges.append(k)
    return edges


def get_maybe_solvable(vars_in_eq_not_solvable,formula_dictionary):
    '''
    get if a variable is maybe solvable by checking if it contains the "of" keyword

    this could help in situation where we have formulas like:
        - molar_mass_of_chemical = xyz
        - molar_mass = mass / moles
        - mass_of_chemical = abc
        - solve for moles
    
    these are clearly linked, but the hypergraph doesn't know that
    '''
    maybe_solvable = []
    all_terms = getAllTerms(formula_dictionary,distinct=True)
    for i in vars_in_eq_not_solvable:
        for j in all_terms:
            if '_of_' in i:
                check_var = re.split('_of_',i)[0]
                if check_var.strip() == j.strip():
                    maybe_solvable.append(f'{i} = {check_var}')
            elif '_of_' in j:
                check_var = re.split('_of_',j)[0]
                if check_var.strip() == i.strip():
                    maybe_solvable.append(f'{j} = {check_var}')
    return maybe_solvable

def add_formula_strings(formula_strings):
    vars_solvable = {}
    i = 0
    for fs in re.split(';',formula_strings):
        lhs,rhs = re.split('=',fs)
        try:
            f_rhs = float(rhs)
            vars_solvable[lhs.strip()] = f'eq{i}'
        except:
            do_nothing = 0
        i += 1
    return vars_solvable

def get_max_formula(formulas):
    max_eq = -1
    for k,v in formulas.items():
        if k[0:2] == 'eq':
            try:
                i_eq = float(k[2:])
                if i_eq > max_eq:
                    max_eq = i_eq
            except:
                do_nothing = 0
    if max_eq != -1:
        return f'eq{int(max_eq)}'
    else:
        return None


def traverseFormulaHypergraph(formula_strings,var):
    formula_dictionary = formulas2Dictionary(formula_strings)
    formula_hypergraph = formulaDictionary2Hypergraph(formula_dictionary)
    vars_solvable = {}
    def traverse(vars_solvable,all_paths,metadata,formula_strings,formulas,fhg,assumptions):
        '''
        traverse through the hyepergraph and find all solvable variables
        '''
        vars_looked_at = []
        edges_looked_at = []
        potential_missing_info = []
        current_path = []
        #add var to stack for breadth first search through hypergraph
        stack = [var]
        i = 0
        #continue until stack is empty
        while len(stack) > 0:
            i += 1
            #get last variable of interest (voi) from stack
            voi = stack.pop()
            #keep track of all variables and edges looked at
            vars_looked_at.append(voi)
            edges = get_edges(fhg,voi)
            #loop through edges
            for edge in edges:
                #get neighbors of edge (variables in equation)
                neighbors = fhg[edge]
                #see what variables in equation are already solvable
                vars_in_eq_not_solvable = [i for i in neighbors if i not in vars_solvable]
                vars_in_eq_solvable = [i for i in neighbors if i in vars_solvable]
                #look for variables that are maybe solvable
                maybe_solvable = get_maybe_solvable(vars_in_eq_not_solvable,formulas)
                #loop through maybe solvable variables and see i you can add it to the formula hyerpgraph
                for ms in maybe_solvable:
                    lhs,rhs = re.split('=',ms)
                    if ms not in formula_strings:
                        formula_strings = formula_strings + ';' + ms
                        formulas = formulas2Dictionary(formula_strings)
                        max_formula = get_max_formula(formulas)
                        #print(formulas)
                        fhg = formulaDictionary2Hypergraph(formulas)
                        vars_solvable[lhs] = max_formula
                
                if len(neighbors) == 1:
                    #if there is only 1 variable in the equation, then it is solvable by definition
                    if current_path + [edge] not in all_paths:
                        current_path.append(edge)
                        vars_solvable[neighbors[0]] = edge
                elif len(vars_in_eq_not_solvable) ==1:
                    #if there is only 1  variable that is not solvable, then you can solve for it
                    if current_path + [edge] not in all_paths:
                        current_path.append(edge)
                        vars_solvable[[i for i in neighbors if i not in vars_solvable][0]] = edge
                elif len(vars_in_eq_not_solvable) == 2 and 'molar_mass_of_chemical' in vars_in_eq_not_solvable and len(metadata) > 0:
                    if current_path + [edge] not in all_paths:
                        current_path.append(edge)
                        vars_solvable[[i for i in neighbors if i not in vars_solvable][0]] = edge
                else:
                    #else then you need to look at the neighbors of the variable
                    for neighbor in neighbors:
                        if neighbor not in vars_solvable and neighbor not in stack and edge not in edges_looked_at and neighbor != voi:
                            stack.append(neighbor)
                edges_looked_at.append(edge)
                if len(vars_in_eq_not_solvable) == 2 and len(vars_in_eq_solvable) > 0:
                    potential_missing_info.extend(vars_in_eq_not_solvable)
        return vars_solvable,potential_missing_info,current_path,formula_strings,formulas,fhg

    #continue to traverse the hypergraph until you find the variable of interest or you can't find any more variables
    #cap at 100 iterations to prevent infinite loop
    j = 0
    while var not in vars_solvable and j < 100:
        j += 1
        old_len = len(vars_solvable)
        vars_solvable,potential_missing_info,current_path,formula_strings,formula_dictionary,formula_hypergraph = traverse(vars_solvable,[],[],formula_strings,formula_dictionary,formula_hypergraph,[])
        if old_len == len(vars_solvable):
            #if you did not add any new variables last iteration, then you are done
            break
    return vars_solvable

if __name__ == '__main__':
    formula_strings = 'miles_per_hour=60;time_in_hours=2;distance_travelled=miles_per_hour*time_in_hours'
    var = 'distance_travelled'
    vars_solvable = traverseFormulaHypergraph(formula_strings,var)
    print(vars_solvable)