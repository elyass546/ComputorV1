import re
import sys


def main():
    # Request input from the user
    if len(sys.argv) != 2:
        print("Invalid input: Please enter a valid polynomial equation")
        return

    # Validate and parse the input equation
    validFormat = check_term_format(sys.argv[1])

    # Print the reduced form of the polynomial
    print_reduced_form(validFormat)

    # Determine the degree of the polynomial
    if validFormat:
        poly_degree = max(validFormat.keys())
    else:
        poly_degree = 0

    print("Polynomial degree:", poly_degree)

    # Solve based on the degree of the polynomial
    if poly_degree > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
    elif poly_degree == 2:
        solve_polynomial(validFormat)
    elif poly_degree == 1:
        print("The solution is:")
        solve_polynomial(validFormat)
    elif poly_degree == 0:
        coeff = validFormat.get(0, 0)
        if coeff == 0:
            print("All real numbers are solutions.")
        else:
            print("No solution.")


def solve_polynomial(terms):
    # Ensure we have terms for X^2, X^1, and X^0 (constant)
    a = terms.get(2, 0)
    b = terms.get(1, 0)
    c = terms.get(0, 0)

    if a != 0:
        # Implement quadratic formula: ax^2 + bx + c = 0
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            real_part = -b / (2 * a)
            imaginary_part = ((-discriminant) ** 0.5) / (2 * a)
            real_str = format_number(real_part)
            imag_str = format_number(imaginary_part)
            # Format the solutions
            solution1 = f"{real_str} + {imag_str}i"
            solution2 = f"{real_str} - {imag_str}i"
            print("Discriminant is strictly negative, the two complex solutions are:")
            print(solution1)
            print(solution2)
        elif discriminant == 0:
            solution = -b / (2 * a)
            solution_str = format_number(solution)
            print("Discriminant is zero, the solution is:")
            print(solution_str)
        else:
            sqrt_disc = discriminant ** 0.5
            solution1 = (-b + sqrt_disc) / (2 * a)
            solution2 = (-b - sqrt_disc) / (2 * a)
            print("Discriminant is strictly positive, the two solutions are:")
            print(format_number(solution1))
            print(format_number(solution2))

    elif b != 0:
        solution = -c / b
        print(format_number(solution))
    elif c == 0:
        print("All real numbers are solutions.")
    else:
        print("No solution.")


def print_reduced_form(polynomial_dict):
    if not polynomial_dict:
        print("Reduced form: 0 = 0")
        return

    terms = []
    for degree in sorted(polynomial_dict.keys()):
        coeff = polynomial_dict[degree]
        sign = '+' if coeff > 0 else '-'
        coeff_str = format_coefficient(my_abs(coeff))
        terms.append(f"{sign} {coeff_str} * X^{degree}")

    # Join terms and remove leading '+' if present
    result = " ".join(terms).strip()
    if result.startswith('+'):
        result = result[1:].strip()  # Remove leading '+'

    print("Reduced form:", result + " = 0")


def check_term_format(equation):
    # Remove spaces from the equation
    equation = equation.replace(' ', '')

    # Split the equation into left-hand side (lhs) and right-hand side (rhs)
    if '=' not in equation:
        return None  # Invalid input

    lhs, rhs = equation.split('=')

    # Find terms in the left-hand and right-hand sides using regular expressions
    lterm_pattern = re.findall(r"([+-]?\d*\.?\d+|\+|\-)?(\*X\^)(\d+)", lhs)
    rterm_pattern = re.findall(r"([+-]?\d*\.?\d+|\+|\-)?(\*X\^)(\d+)", rhs)

    # Move all terms from RHS to LHS and flip their signs
    lhs_new = move_terms_to_lhs(lterm_pattern, rterm_pattern)
    if lhs_new is None:
        return None  # Return None if the format is invalid
    return lhs_new


def move_terms_to_lhs(lterm_pattern, rterm_pattern):
    lhs_dict = {}

    # Check if both patterns are empty, indicating invalid input
    if not lterm_pattern and not rterm_pattern:
        return None

    # Process LHS terms and directly add them to the dictionary
    for coeff_str, _, degree in lterm_pattern:
        coeff = parse_coefficient(coeff_str)
        add_term_to_dict(lhs_dict, coeff, degree)

    # Process RHS terms, flip their signs, and then add to the LHS dictionary
    for coeff_str, _, degree in rterm_pattern:
        coeff = parse_coefficient(coeff_str)
        # Flip the sign numerically
        coeff = -coeff
        add_term_to_dict(lhs_dict, coeff, degree)

    # Remove terms with zero coefficients
    lhs_dict = {deg: coeff for deg, coeff in lhs_dict.items() if coeff != 0}

    return lhs_dict


def parse_coefficient(coeff_str):
    """
    Parses the coefficient string into a float, handling optional signs.
    """
    if coeff_str in ('', '+', '-'):
        # Coefficient is implied to be +1 or -1
        return 1.0 if coeff_str != '-' else -1.0
    else:
        try:
            return float(coeff_str)
        except ValueError:
            # Handle cases where coeff_str is '0'
            if coeff_str == '0':
                return 0.0
            else:
                return None  # Invalid coefficient


def add_term_to_dict(terms_dict, coeff, degree):
    """
    Helper function to add a term to the dictionary of terms.
    """
    if coeff is None:
        return  # Skip invalid coefficients
    degree = int(degree)

    if degree in terms_dict:
        terms_dict[degree] += coeff
    else:
        terms_dict[degree] = coeff


def my_abs(number):
    """
    Computes the absolute value of a number without using the built-in abs().
    """
    return -number if number < 0 else number


def format_coefficient(coef):
    """
    Formats a coefficient by converting it to an integer if it is equivalent
    to an integer, otherwise leaves it as a float.
    """
    if coef == int(coef):
        return str(int(coef))
    else:
        return str(coef)


def format_number(num):
    """
    Formats a number by converting it to an integer if it is equivalent
    to an integer, otherwise formats it as a float with up to 6 decimal places,
    removing unnecessary trailing zeros.
    """
    if num == int(num):
        return str(int(num))
    else:
        return "{0:.6f}".format(num).rstrip('0').rstrip('.')


# Run the main function when the script is executed
if __name__ == "__main__":
    main()
