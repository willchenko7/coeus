'''
Goal: execute a single step in the solving plan.

Input:
    problem: a string containing a problem statement

Output:
    answer: a string containing the answer to the problem statement

Example:
    problem = 'Solve for radius_of_sphere: volume_of_sphere=radius_of_sphere*3.14'
    
    answer = 'radius_of_sphere = volume_of_sphere/3.14'
'''

import re
from solver import solver
from simplify_formula import simplify_formula

def check_if_var_solved(answer,var):
    '''
    helper fn to see if the variable of interest is solved
    '''
    var = var.strip()
    answer = answer.strip()
    answer = answer.replace(' ','')
    if answer.startswith(f'{var}=') or answer.endswith(f'={var}'):
        return True
    else:
        return False

def singleStep(problem):
    #clean problem
    problem = problem.replace('−', '-')

    #get var and eq from problem
    problem_parts = re.split(': ',problem.replace('-->',''))
    words = problem_parts[0]
    var = re.split(' ',words)[-1]
    eq = problem_parts[1]
    known_coeff_dict = {}

    #see if it is already solved
    answer = eq
    var_solved = check_if_var_solved(answer,var)
    if var_solved == True:
        answer = simplify_formula(answer)
        return answer
    
    #solve for the variable of interest using the solver fn
    answer = solver(eq,var)
    answer = simplify_formula(answer)
    return answer

if __name__ == '__main__':
    problem = 'Solve for radius_of_sphere: volume_of_sphere=radius_of_sphere*3.14'
    answer = singleStep(problem)
    print('FINAL ANSWER')
    print(answer)
    print('----')