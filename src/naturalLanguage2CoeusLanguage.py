'''

Goal: convert a question in natural language to a coeus language question.

Coeus Language (CL) is a language that is used to represent the question in a way that is easy to parse and understand for the mathematical solver.

Input:
    - question in natural language
    - model - the model to use to condense the question. Default is gpt-4-0314

Output:
    - CL question

Example:
    Input:  "If a car is traveling at 60 miles per hour, how many miles will it travel in 2 hours?"

    Output: "Solve for distance_travelled: miles_per_hour=60;time_in_hours=2;distance_travelled=miles_per_hour*time_in_hours"

'''
from src.condenseQuestion import condenseQuestion
from src.condensed2CoeusLanguage import condensed2CoeusLanguage

def naturalLanguage2CoeusLanguage(question,model="gpt-4-0314"):
    #condense the question
    condensed_sentence,total_tokens = condenseQuestion(question,model)
    #convert the condensed question to coeus language
    coeus_sentence = condensed2CoeusLanguage(condensed_sentence)
    return coeus_sentence
