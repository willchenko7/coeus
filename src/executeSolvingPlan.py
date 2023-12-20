'''

Goal: given a solving plan, loop through eac step and solve for the variable of interest

'''
import re
from singleStep import singleStep
from simplify_formula import simplify_formula

def fillFormulaWithCoefficients(formula, coeff_dict):
    '''
    helper fn to replace variables in a formula with their values from coeff_dict
    '''
    formula = formula.replace(' ','')
    def repl(match):
        # The matched word (coefficient) is match.group(0)
        coeff = match.group(0)
        return str(coeff_dict.get(coeff, coeff))

    # The pattern matches any word that appears as a key in coeff_dict
    pattern = r'\b(' + '|'.join(map(re.escape, coeff_dict.keys())) + r')\b'
    return re.sub(pattern, repl, formula)

def executeSolvingPlan(solve_statements,var):
    coeff_dict = {}
    i_ss = 0
    #loop through each step in the solving plan
    for q in solve_statements:
        print(f'Step {i_ss}: {q}')
        i_ss += 1
        #get the variable of interest for this step
        voi = re.split(' ',re.split(':',q)[0])[-1]
        #try to solve for the variable of interest
        try:
            a = singleStep(q)
        except:
            a = 'NA'
        #add vars it solved for to the coeff_dict
        if '=' in a and voi != var:
            v1,v2 = re.split('=',a)
            if v1.strip() == voi:
                coeff_dict[voi] = v2.strip()
            elif v2.strip() == voi:
                coeff_dict[voi] = v1.strip()

    #simplify coeff_dict
    for k,v in coeff_dict.items():
        vs = [i for i in v if i.isalpha()]
        for i in vs:
            if i in coeff_dict:
                v = v.replace(i,'(' + coeff_dict[i] + ')')
                coeff_dict[k] = v

    for k,v in coeff_dict.items():
        coeff_dict[k] = '(' + v + ')'
    
    #replace terms in answer with values from coeff_dict
    i = 0
    while i < 100:
        i+=1
        #print(f'i: {i}')
        old_a = a
        a = fillFormulaWithCoefficients(a, coeff_dict)
        if a == old_a:
            break
    #simplify answer 
    a = a.replace('s*q*r*t','sqrt')
    a = simplify_formula(a)
    return a

if __name__ == '__main__':
    var = 'distance_travelled'
    solve_statements = ['Solve for time_in_hours: time_in_hours=2 -->', 'Solve for miles_per_hour:  miles_per_hour=60 -->', 'Solve for distance_travelled: distance_travelled=miles_per_hour*time_in_hours -->']
    a = executeSolvingPlan(solve_statements,var)
    print(a)