import re

'''

Goal: convert a coeus language question to a dictionary where the keys are equation names and the values are the equations

Input:
    - coeus language question

Output:
    - dictionary where the keys are equation names and the values are the equations

Example:
    Input:  "miles_per_hour=60;time_in_hours=2;distance_travelled=miles_per_hour*time_in_hours"

    Output: {'eq0': 'miles_per_hour=60', 'eq1': 'time_in_hours=2', 'eq2': 'distance_travelled=miles_per_hour*time_in_hours'}

'''

def formulas2Dictionary(formula_strings):
    all_formulas = []
    formula_strings = re.split(';',formula_strings)
    dictionary = {}
    counter = 0
    for formula_string in formula_strings:
        if formula_string not in all_formulas:
            equation_name = f'eq{counter}'
            dictionary[equation_name] = formula_string
            all_formulas = formula_string
            counter += 1
    return dictionary

if __name__ == '__main__':
    formula_strings = "miles_per_hour=60;time_in_hours=2;distance_travelled=miles_per_hour*time_in_hours"
    dictionary = formulas2Dictionary(formula_strings)
    print(dictionary)