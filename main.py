import re

def check_for_foreign_characters(equation):
    allowed_characters = set("=+-*X^ 0123456789")
    
    # Check if there are any characters in 'equation' that are not in 'allowed_characters'
    for char in equation:
        if char not in allowed_characters:
            raise ValueError(f"Error: Invalid character '{char}' found in the input.")


def parse_equation(equation):
    # Checking for foreign Characters
    try:
        check_for_foreign_characters(equation)
    except ValueError as e:
        print(e)

    # Split the equation into left and right sides at the equals sign
    lhs, rhs = equation.split('=')

    # Clean up whitespaces
    lhs = lhs.replace(' ', '')
    rhs = rhs.replace(' ', '')

    # Parse each side of the equation and combine into a standard form
    lhs_terms = parse_polynomial(lhs)
    rhs_terms = parse_polynomial(rhs)

    # Move all terms to one side (subtract right side from left side)
    for power in rhs_terms:
        if power in lhs_terms:
            lhs_terms[power] -= rhs_terms[power]
        else:
            lhs_terms[power] = -rhs_terms[power]

    return lhs_terms

def parse_polynomial(poly):
    # Find terms like "5", "4*X^1", "X^2", "+X", "-X"
    term_pattern = re.compile(r'([+-]?\d*\.?\d*)\*?X\^?(\d*)')
    terms = {}

    for match in term_pattern.findall(poly):
        coeff = match[0]
        power = match[1] if match[1] else '1'

        # Handle cases where coefficient is empty (like "+X" or "-X")
        if coeff == '+' or coeff == '':
            coeff = 1.0
        elif coeff == '-':
            coeff = -1.0
        else:
            coeff = float(coeff)

        power = int(power) if power else 1

        if power in terms:
            terms[power] += coeff
        else:
            terms[power] = coeff

    return terms


def solve_polynomial(terms):
    # Ensure we have terms for X^2, X^1, and X^0 (constant)
    a = terms.get(2, 0)
    b = terms.get(1, 0)
    c = terms.get(0, 0)

    if (a != 0):
        # Implement quadratic formula: ax^2 + bx + c = 0
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            print("No real solutions")
        elif discriminant == 0:
            solution = -b / (2 * a)
            print(f"One solution: x = {solution}")
        else:
            sqrt_disc = discriminant ** 0.5  # Custom sqrt calculation
            solution1 = (-b + sqrt_disc) / (2 * a)
            solution2 = (-b - sqrt_disc) / (2 * a)
            print(("%.6f" % solution2).rstrip('0').rstrip('.'))
            print(("%.6f" % solution1).rstrip('0').rstrip('.'))
    elif (b != 0):
        solution = -c / b
        print(("%.6f" % solution).rstrip('0').rstrip('.'))
    elif (c != 0):
        if (c == 0):
            print("Infiniten solution (0 = 0)")
        else:
            print("No solution (c != 0)") 

def print_reduced_form(polynomial_dict):
    terms = []
    for degree in sorted(polynomial_dict.keys()):
        coeff = polynomial_dict[degree]
        if coeff != 0:  # Ignore zero coefficients
            sign = '+' if coeff > 0 else ''
            terms.append(f"{sign} {coeff} * X^{degree}")

    # Join terms and remove leading '+' if present
    result = " ".join(terms).strip()
    if result.startswith('+ '):
        result = result[2:]  # Remove leading '+'

    print("Reduced form: ", result + " = 0")

def check_term_format(equation):
    # Regular expression to match terms in the form 'a * X^p', allowing optional spaces after + or -
    term_pattern = re.compile(r'^[+-]?\s*\d+(\.\d+)?\s*\* X\^\d+$')
    
    # Split the equation into left-hand side (lhs) and right-hand side (rhs)
    lhs, rhs = equation.split('=')
    
    # Split both sides into terms based on `+` or `-` starting a new term
    lhs_terms = re.split(r'(?=[+-])', lhs.strip())
    rhs_terms = re.split(r'(?=[+-])', rhs.strip())

    # Check LHS terms if they match the expected format "a * X^p"
    for term in lhs_terms:
        term = term.strip()  # Strip any leading/trailing spaces
        if not term_pattern.match(term):
            return False

    # Check RHS terms if they match the expected format "a * X^p"
    for term in rhs_terms:
        term = term.strip()  # Strip any leading/trailing spaces
        if not term_pattern.match(term):
            return False

    return True

# Example Usage
# equation = "1 * X^2 - 2 * X^1 - 24 * X^0 = 0"
equation = "5 * X^2 + 2 * X^1 - 5 * X^0 = 3 * X^2 + 4 * X^1 + 7 * X^0"


validFormat = check_term_format(equation)

if not validFormat:
    print("Invalid input: the equation must follow the format 'a * X^p'.")
    exit()

parsed_terms = parse_equation(equation)

print_reduced_form(parsed_terms)

poly_degree = max(parsed_terms.keys())

print("Polynomial degree: ", poly_degree)

if poly_degree > 2:
    print("The polynomial degree is strictly greater than 2, I can't solve.")
elif poly_degree == 2:
    print("Discriminant is strictly positive, the two solutions are:")
    solve_polynomial(parsed_terms)
elif poly_degree == 1:
    print("The solution is:")
    solve_polynomial(parsed_terms)