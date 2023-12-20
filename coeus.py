'''
Coeus aims to be a answer questions in natural language by combining the power of symbolic math and llm's

Input:
    - question in natural language

Output:
    - answer with steps printed out
'''
import re
import sys
sys.path.append('src')
from src.naturalLanguage2CoeusLanguage import naturalLanguage2CoeusLanguage
from src.coeusLanguage2Hypergraph import coeusLanguage2Hypergraph
from src.traverseFormulaHypergraph import traverseFormulaHypergraph
from src.executeSolvingPlan import executeSolvingPlan
from src.fillOutHypergraphPath import fillOutHypergraphPath

def coeus(question):
    print(f'Question in natural language: {question}')
    print('---')
    #convert question to Coeus language
    question = naturalLanguage2CoeusLanguage(question)
    print(f'Question in Coeus language: {question}')
    #split the question into the desired variable and the formulas
    problem_parts = re.split(': ',question.replace('-->',''))
    words = problem_parts[0]
    var = re.split(' ',words)[-1]
    formula_strings = problem_parts[1]
    #get the hypergraph and dictionary representation of the formulas
    formula_hypergraph,formula_dictionary = coeusLanguage2Hypergraph(question)
    #traverse the hypergraph to find solving plan
    path = traverseFormulaHypergraph(formula_strings,var)
    #fill out solving plan
    solving_plan = fillOutHypergraphPath(path,formula_dictionary,var)
    #execute the solving plan
    answer = executeSolvingPlan(solving_plan,var)
    print('---')
    print(f'Answer: {answer}')
    return answer

if __name__ == '__main__':
    question = "If a car is traveling at 60 miles per hour, how many miles will it travel in 2 hours?"
    coeus(question)