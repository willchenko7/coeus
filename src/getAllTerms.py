'''
Goal: from a given formnula dictionary, get all terms. optionally, get distinct terms only

Inputs:
    - formula dictionary
    - distinct (default True)

Outputs:
    - list of terms

Example:
    - input: {'eq0': ' mass_of_nacl=58.44g', 'eq1': 'volume_of_solution=1l'}
    - output: ['mass_of_nacl','volume_of_solution','g','l']
'''

import re

def getAllTerms(formula_dictionary,distinct=True):
    all_terms = []
    for k,v in formula_dictionary.items():
        v = v.replace('*',' ')
        v = v.replace('-',' ')
        v = v.replace('+',' ')
        v = v.replace('/',' ')
        v = v.replace('^',' ')
        v = v.replace('=',' ')
        v = v.replace('sin','')
        v = v.replace('cos','')
        vs = re.split(' ',v)
        for vsi in vs:
            vsi = ''.join([i for i in vsi if i.isalpha() or i =='_'])
            vsi = vsi.replace(' ','')
            if vsi != '':
                all_terms.append(vsi)
    if distinct == True:
        return list(set(all_terms))
    else:
        return all_terms
    
if __name__== '__main__':
    formula_dictionary = {'eq0': ' mass_of_nacl=58.44g', 'eq1': 'volume_of_solution=1l'}
    print(getAllTerms(formula_dictionary))