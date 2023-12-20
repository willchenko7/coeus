

def simplify_formula(formula):
    '''
    simplfy expression by evaluating the lhs and rhs
    '''
    formula = formula.replace('^','**')
    try:
        # Extract variable and expression
        var, expression = formula.split('=')
        #evaluate rhs
        try:
            rhs = eval(expression)
        except:
            rhs = expression
        #evalute lhs
        try:
            lhs = eval(var)
        except:
            lhs = var
        
        return f'{str(lhs).strip()} = {str(rhs).strip()}'
    except:
        return formula