'''

Goal: solve for the variable of interest in a given equation using sympy.

It can also solve for derivatives and integrals

Input:
    - formula: str
    - var: str

Output:
    - answer: str

Example:
    formula  = 'x = 6-(5.0+x)'
    var = 'x'

    answer = 'x = 0.5'
'''

from sympy import symbols, Eq, solve, parse_expr,diff,integrate
import re

def isDiff(var):
    if '/' not in var:
        return None,None,None
    u,l = re.split('/',var)
    if u[0] == 'd' and l[0] == 'd':
        if '^' not in var:
            return u[1:],l[1:],1
        else:
            return re.split('\^',u)[1][1:],re.split('\^',l)[0][1:],int(re.split('\^',l)[1])
    return None,None,None

def isIntegral(formula,var):
    #assumes max of 2 d(vars)
    if 'd' + var not in formula:
        return None, None
    dvars = []
    s_current = None
    for char in formula:
        #print(f'Char: {char}')
        #print(f's_current: {s_current}')
        if char == 'd':
            s_current = 'd'
        elif s_current is not None and char.isalpha():
            s_current = s_current + char
        elif s_current is not None:
            dvars.append(s_current)
            s_current = None
    if s_current is not None:
        dvars.append(s_current)
    #print(dvars)
    if 'd' + var == dvars[0]:
        return dvars[0],dvars[1]
    else:
        return dvars[1],dvars[0]

def diff_solver(formula,uv,lv,diff_order):
    new_formula = solver(formula,uv)
    lhs_str, rhs_str = new_formula.split('=')
    lhs = parse_expr(lhs_str.strip())
    rhs = parse_expr(rhs_str.strip())
    d_lhs = diff(lhs,symbols(uv),diff_order)
    d_rhs = diff(rhs,symbols(lv),diff_order)
    if diff_order != 1:
        deriv_term = f'd^{diff_order}{uv}/d{lv}^{diff_order}'
    else:
        deriv_term = f'd{uv}/d{lv}'
    if diff_order == 1 and str(d_lhs) == '1':
        new_lhs = ''
    elif diff_order > 1 and str(d_lhs) == '0':
        new_lhs = ''
    else:
        new_lhs = str(d_lhs)
    new_rhs = str(d_rhs)
    answer = f'{new_lhs}{deriv_term} = {new_rhs}'
    return answer

def integration_solver(formula,uv,lv):
    new_formula = solver(formula,uv)
    lhs_str, rhs_str = new_formula.split('=')
    lhs = parse_expr(lhs_str.strip())
    rhs = parse_expr(rhs_str.strip())
    i_lhs = integrate(lhs,symbols(uv[1:]))
    i_rhs = integrate(rhs,symbols(lv[1:]))
    new_lhs = str(i_lhs)
    new_lhs = new_lhs.replace(uv + '*','')
    new_lhs = new_lhs.replace('*' + uv,'')
    new_lhs = new_lhs.replace(uv,'')
    new_rhs = str(i_rhs)
    new_rhs = new_rhs.replace(lv + '*','')
    new_rhs = new_rhs.replace('*' + lv,'')
    new_rhs = new_rhs.replace(lv,'')
    answer = f'{new_lhs} = {new_rhs} + C'
    return answer

def replace_keywords(formula):
    keywords = ['sin','cos','tan','log','ln','asin','acos','atan']
    for keyword in keywords:
        formula = formula.replace(''.join([i +' ' for i in keyword]),keyword)
    return formula

def solver(formula,var):
    formula = formula.replace(' ','')
    formula = replace_keywords(formula)
    uv,lv,diff_order = isDiff(var)
    if uv is not None:
        answer = diff_solver(formula,uv,lv,diff_order)
        return answer
    uv,lv = isIntegral(formula,var)
    if uv is not None:
        answer = integration_solver(formula,uv,lv)
        return answer
    formula = formula.replace('^','**')
    lhs_str, rhs_str = formula.split('=')
    lhs = parse_expr(lhs_str.strip())
    rhs = parse_expr(rhs_str.strip())
    equation = Eq(lhs, rhs)
    all_symbols = list(equation.free_symbols)
    symbol_dict = {str(sym): sym for sym in all_symbols}
    solution = solve(equation,symbol_dict[var])
    answer = f'{var} = {str(solution[0])}'
    return answer
 
if __name__ == '__main__':
    #formula = '( A * x^2 ) * ( C * x ) = F'
    #formula = 'dy = sin(x)*dx'
    formula  = 'x = 6-(5.0+x)'
    var = 'x'
    answer = solver(formula,var)
    print(f'Answer: {answer}')