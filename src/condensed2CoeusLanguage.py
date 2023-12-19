'''

Goal: convert the condensed question (output of condenseQuestion) to a coeus language question.

Coeus Language (CL) is a language that is used to represent the question in a way that is easy to parse and understand for the mathematical solver.

Input:
    - condensed question (output of condenseQuestion)

Output:
    - CL question

Example:
    Input:  "<start>desired_variable=distance_travelled;miles_per_hour=60;time_in_hours=2;distance_travelled=miles_per_hour*time_in_hours<stop>"
    Output: "Solve for distance_travelled: miles_per_hour=60;time_in_hours=2;distance_travelled=miles_per_hour*time_in_hours"

'''

import re

def condensed2CoeusLanguage(condensed_sentence):
    #lowercase everything
    cs = condensed_sentence.lower()
    #remove start and stop tags
    cs = cs.replace('<start>','')
    cs = cs.replace('<stop>','')
    #split by semicolons
    vs = re.split(';',cs)
    formulas = []
    var = None
    for voi in vs:
        #split voi by equal sign
        lhs,rhs = re.split('=',voi)
        if lhs == 'desired_variable':
            #this is the variable we want to solve for
            var = rhs
        elif rhs == '??' or rhs == '?':
            #this is a variable that we don't know
            do_nothing = 0
        else:
            #this is a formula we can use to solve for the desired variable
            value = re.split(' ',rhs)[0]
            formulas.append(f"{lhs}={value}")
    #format the output
    coeus_sentence = f"Solve for {var}: {';'.join(formulas)}"
    return coeus_sentence

if __name__ == '__main__':
    condensed_sentence = "<start>desired_variable=distance_travelled;miles_per_hour=60;time_in_hours=2;distance_travelled=miles_per_hour*time_in_hours<stop>"
    coeus_sentence = condensed2CoeusLanguage(condensed_sentence)
    print(coeus_sentence)