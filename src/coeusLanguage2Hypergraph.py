'''
Goal: convert a coeus language question to a hypergraph and a dictionary representation

Input:
    - coeus language question

Output:
    - hypergraph
    - dictionary

Example:
    Input:  "Solve for distance_travelled: miles_per_hour=60;time_in_hours=2;distance_travelled=miles_per_hour*time_in_hours"

    Output: 
        - {
            'eq0': ['miles_per_hour'], 
            'eq1': ['time_in_hours'], 
            'eq2': ['distance_travelled', 'miles_per_hour', 'time_in_hours']
        }
        - {'eq0': 'miles_per_hour=60', 'eq1': 'time_in_hours=2', 'eq2': 'distance_travelled=miles_per_hour*time_in_hours'}

'''

from formulas2Dictionary import formulas2Dictionary
from formulaDictionary2Hypergraph import formulaDictionary2Hypergraph

def coeusLanguage2Hypergraph(coeus_language_question):
    #split the question into the desired variable and the formulas
    desired_variable,formulas = coeus_language_question.split(':')
    #remove the 'solve for' from the desired variable
    desired_variable = desired_variable.replace('solve for ','')
    #convert the formulas to a dictionary
    formula_dictionary = formulas2Dictionary(formulas)
    #convert the dictionary to a hypergraph
    formula_hypergraph = formulaDictionary2Hypergraph(formula_dictionary)
    return formula_hypergraph,formula_dictionary

if __name__ == '__main__':
    coeus_language_question = "Solve for distance_travelled: miles_per_hour=60;time_in_hours=2;distance_travelled=miles_per_hour*time_in_hours"
    formula_hypergraph,formula_dictionary = coeusLanguage2Hypergraph(coeus_language_question)
    print(formula_hypergraph)
    print(formula_dictionary)