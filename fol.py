import re

def tokenize(sentence):
    # Split a FOL sentence into its function and terms
    func_name, terms = sentence[:-1].split('(', 1)
    terms = terms.split(',')
    return func_name, [term.strip() for term in terms]

def unify_var(var, x, substitution):
    # If var is already in substitution, we need to unify the term with what it's mapped to
    if var in substitution:
        return unify(substitution[var], x, substitution)
    # If x is already in substitution, unify var with x's mapped term
    elif x in substitution:
        return unify(var, substitution[x], substitution)
    # Otherwise, we map var to x
    elif var != x:
        substitution[var] = x
    return substitution

def unify(term1, term2, substitution=None):
    if substitution is None:
        substitution = {}

    # If terms are identical, return the substitution as is
    if term1 == term2:
        return substitution

    # Check if term1 is a variable
    if re.match(r'^[a-z]$', term1):
        return unify_var(term1, term2, substitution)
    
    # Check if term2 is a variable
    if re.match(r'^[a-z]$', term2):
        return unify_var(term2, term1, substitution)

    # Handle negation cases
    if term1.startswith('¬') and term2 == term1[1:]:
        return substitution 
    if term2.startswith('¬') and term1 == term2[1:]:
        return substitution

    if '(' in term1 and '(' in term2:
        func1, args1 = tokenize(term1)
        func2, args2 = tokenize(term2)

        # Ensure functions and argument counts match
        if func1 != func2 or len(args1) != len(args2):
            return {}

        # Unify each argument recursively
        for arg1, arg2 in zip(args1, args2):
            substitution = unify(arg1, arg2, substitution)
            if substitution == {}:
                return {}

        return substitution

    # If terms don't match and are not variables or compound terms, unification fails
    print(f"Failed to unify: {term1} with {term2}")
    return {}

   
"""
def negate_literal(literal):
    print(f"Negating literal: {literal}")
    negated = literal[1:] if literal.startswith('¬') else f'¬{literal}'
    print(f"Result: {negated}")
    return negated
"""

def negate_literal(literal):
    # Negates a literal: if it starts with '¬', remove it; otherwise, add '¬'
    return literal[1:] if literal.startswith('¬') else f'¬{literal}'

def negate(query):
    # Negate each literal in the clause
    return frozenset(negate_literal(lit) for lit in query)

def apply_single_substitution(literal, substitution):
    """ Apply a single substitution to a literal. """
    # If it's a variable, return the substitution value
    if literal in substitution:
        return substitution[literal]

    # If it's a compound term, tokenize and apply substitutions to arguments
    if '(' in literal:
        func_name, terms = tokenize(literal)
        substituted_terms = [apply_single_substitution(term, substitution) for term in terms]
        return f"{func_name}({','.join(substituted_terms)})"

    return literal

def apply_substitution(clause, substitution):
    """ Apply the substitution to each literal in the clause. """
    return frozenset(apply_single_substitution(literal, substitution) for literal in clause)

def resolve_clause(clause1, clause2):
    """Attempt to resolve two clauses and return the resolvents."""
    resolvents = set()
    
    for literal in clause1:
        if f'¬{literal}' in clause2:
            # Create a new clause without the complementary literals
            new_clause = (clause1 - {literal}) | (clause2 - {f'¬{literal}'})
            resolvents.add(frozenset(new_clause))
    
    return resolvents
    

def inference_by_resolution(kb, query):
    """Perform resolution to infer the truth of the query."""
    negated_query = negate(query)

    # Initialize clauses with knowledge base and negated query
    clauses = kb | {negated_query}

    while True:
        new_resolvents = set()
        
        # Iterate over pairs of clauses for resolution
        for clause1 in clauses:
            for clause2 in clauses:
                if clause1 != clause2:
                    # Resolve the clauses
                    resolvents = resolve_clause(clause1, clause2)

                    if frozenset() in resolvents:
                        # If an empty clause is found, return True
                        return True
                    
                    new_resolvents.update(resolvents)
        
        # Check if any new resolvents were found
        if new_resolvents.issubset(clauses):
            return False 
        
        clauses = clauses | new_resolvents 

    return False


def main():
    print(unify('Parent(x, y)', 'Parent(John, Mary)'))  # Expected output: {'x': 'John', 'y': 'Mary'}
    print(unify('Loves(father(x), x)', 'Loves(father(John), John)'))  # Expected output: {'x': 'John'}
    print(unify('Parent(x, x)', 'Parent(John, Mary)'))  # Expected output: {}

    kb = {
    frozenset({'¬King(x)', '¬Greedy(x)', 'Evil(x)'}),
    frozenset({'King(John)'}),                           
    frozenset({'Greedy(x)'})                             
    }

    query = frozenset({'Evil(John)'})

    
    result = inference_by_resolution(kb, query)
    print("Evil(John) is", result)  # Expected output: True, 
    #although based on the first cnf sentence isnt john not evil becuase he is a king? rather than not a king

    kb_simple = {frozenset({'A'}), frozenset({'¬A', 'C'})}
    query_simple = frozenset({'C'})
    print(inference_by_resolution(kb_simple, query_simple))  # Should be True

if __name__ == '__main__':
    main()