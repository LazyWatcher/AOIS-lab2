import itertools
import re

def evaluate(op, a, b=None):
    if b is None:
        if op == '!':
            return not a
        return False
    if op == '&':
        return a and b
    if op == '|':
        return a or b
    if op == '~':
        return a == b
    if op == '-':
        return not a or b
    return False

def precedence(op):
    if op in ('!', '~'):
        return 3
    if op in ('&'):
        return 2
    if op in ('|', '-'):
        return 1
    return 0

def apply_operator(operators, operands):
    op = operators.pop()
    if op == '!':
        a = operands.pop()
        operands.append(evaluate(op, a))
    else:
        b = operands.pop()
        a = operands.pop()
        operands.append(evaluate(op, a, b))

def evaluate_expression(expression, values, variables):
    operands = []
    operators = []

    i = 0
    while i < len(expression):
        if expression[i] == ' ':
            i += 1
            continue
        if expression[i] == '(':
            operators.append(expression[i])
        elif expression[i] == ')':
            while operators and operators[-1] != '(':
                apply_operator(operators, operands)
            operators.pop()
        elif expression[i] in variables:
            operands.append(values[variables.index(expression[i])])
        elif expression[i] == '!':
            operators.append(expression[i])
        else:
            while (operators and precedence(operators[-1]) >= precedence(expression[i])):
                apply_operator(operators, operands)
            operators.append(expression[i])
        i += 1

    while operators:
        apply_operator(operators, operands)

    return operands[-1]

def extract_variables(expression):
    return sorted(set(re.findall(r'[a-z]', expression)))

def print_truth_table(expression):
    variables = extract_variables(expression)
    num_vars = len(variables)
    table_results = []

    for values in itertools.product([False, True], repeat=num_vars):
        for value in values:
            print(int(value), end=" ")
        result = evaluate_expression(expression, list(values), variables)
        print(" |", int(result))
        table_results.append(result)

    return table_results, variables

def get_num_vars(truth_table_size):
    num_vars = int(truth_table_size).bit_length() - 1
    if (1 << num_vars) != truth_table_size:
        raise ValueError("Неправильный размер таблицы истинности")
    return num_vars

def build_pcnf(truth_table_results, variables):

    scnf = ""
    num_vars = get_num_vars(len(truth_table_results))

    for i, result in enumerate(truth_table_results):
        if result:
            continue

        binary = f"{i:0{num_vars}b}"

        conjunction = ""
        for j in range(num_vars):
            if binary[j] == '0':
                conjunction += f"{variables[j]}"
            else:
                conjunction += f"!{variables[j]}"
            conjunction += " | "
        conjunction = conjunction[:-3]
        if scnf:
            scnf += " & "
        scnf += f"({conjunction})"

    return scnf

def build_pdnf(truth_table_results, variables):
    sdnf = ""
    num_vars = get_num_vars(len(truth_table_results))

    for i, result in enumerate(truth_table_results):
        if not result:
            continue

        binary = f"{i:0{num_vars}b}"

        disjunction = ""
        for j in range(num_vars):
            if binary[j] == '0':
                disjunction += f"!{variables[j]}"
            else:
                disjunction += f"{variables[j]}"
            disjunction += " & "
        disjunction = disjunction[:-3]

        if sdnf:
            sdnf += " | "
        sdnf += f"({disjunction})"

    return sdnf

def print_index_form(truth_table_results):
    binary_form = ''.join(str(int(result)) for result in truth_table_results)
    decimal_form = int(binary_form, 2)
    print(f"Индексная форма: {binary_form} - {decimal_form}")

def get_index_form(truth_table_results):
    binary_form = ''.join(str(int(result)) for result in truth_table_results)
    return binary_form

def get_numerical_form(truth_table_results):
    binary_form = ''.join(str(int(result)) for result in truth_table_results)
    decimal_form = int(binary_form, 2)
    return decimal_form

def print_numerical_form(truth_table_results):
    ones = [i for i, result in enumerate(truth_table_results) if result]
    zeros = [i for i, result in enumerate(truth_table_results) if not result]
    print(f"({', '.join(map(str, zeros))}) &")
    print(f"({', '.join(map(str, ones))}) |")

def main():
    expression = "((!a) & b) | c "
    truth_table_results, variables = print_truth_table(expression)
    print_index_form(truth_table_results)
    print_numerical_form(truth_table_results)
    binary_form = get_index_form(truth_table_results)
    decimal_form = get_numerical_form(truth_table_results)

    pcnf = build_pcnf(truth_table_results, variables)
    print("SKNF:", pcnf)

    pdnf = build_pdnf(truth_table_results, variables)
    print("SDNF:", pdnf)

if __name__ == "__main__":
    main()
