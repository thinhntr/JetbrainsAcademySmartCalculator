from collections import deque


def merge_operators(operators):
    minus_operator_count = 0
    for operator in operators:
        if operator != '-' and operator != '+':
            return False
        if operator == '-':
            minus_operator_count += 1
    return '+' if minus_operator_count % 2 == 0 else '-'


def simplify_expr(infix):
    infix.insert(0, '+')
    infix.insert(0, '0')
    new_expr = []
    redundant_operators = []
    for component in infix:
        if component in '+-':
            redundant_operators.append(component)
        else:
            if redundant_operators:
                new_expr.append(merge_operators(redundant_operators))
                redundant_operators = []
            new_expr.append(component)
    return new_expr


def compare(operator1, operator2):
    return precedence_of(operator1) - precedence_of(operator2)


def precedence_of(operator):
    if operator in '+-':
        return 0
    elif operator in '*/':
        return 1
    elif operator == '^':
        return 2
    else:
        return -1


def infix_to_postfix(expression):
    postfix = []
    stack = deque()
    for component in expression:
        if component.isalpha() or component.isnumeric() or component == '(':
            stack.append(component)
        elif component in '+-*/^':
            while stack and (stack[-1].isalpha() or stack[-1].isnumeric() or compare(stack[-1], component) >= 0):
                postfix.append(stack.pop())
            stack.append(component)
        else:
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()
    while stack:
        postfix.append(stack.pop())
    return postfix


def run(command):
    if command == "/help":
        print("Type in an expression and this program will evaluate it")
        return 'continue'
    elif command == "/exit":
        print("Bye!")
        return 'break'
    else:
        print("Unknown command")
        return 'continue'


def get_value(variable):
    if variable.isnumeric():
        return int(variable)
    if not variable.isalpha():
        return "Invalid assignment"
    return variables.get(variable, 'Unknown variable')


def typeof(character):
    if character.isalpha():
        return 'variable'
    if character.isnumeric():
        return 'number'
    if character in '+-*/^()':
        return 'operator'
    return ' ' if character == ' ' else ''


def next_possible_types(current_component=None):
    if current_component is None:
        return ['variable', 'number', '(', '+', '-']

    if current_component.isalpha() or current_component.isnumeric():
        return [')', '+', '-', '*', '/', '^']

    if current_component in '+-':
        return ['variable', 'number', '+', '-', '(']

    if current_component in '*/^':
        return ['variable', 'number', '(']

    if current_component == '(':
        return ['variable', 'number', '+', '-', '(', ')']

    if current_component == ')':
        return ['+', '-', '*', '/', '^', ')']


def parse(expression):
    infix = []
    start = 0
    current_type = typeof(expression[start])
    for end in range(1, len(expression)):
        if current_type == 'operator' or typeof(expression[end]) != current_type:
            if expression[start] != ' ':
                infix.append(expression[start:end])
            start = end
            current_type = typeof(expression[start])
    infix.append(expression[start:])
    return infix


def check_syntax(infix_expr):
    parentheses = deque()
    error = False
    previous_component = None
    for component in infix_expr:
        if typeof(component) == 'variable' and not variables.get(component):
            error = 'Unknown variable'
            break
        elif typeof(component) == '' or (typeof(component) not in next_possible_types(previous_component)
                                         and component not in next_possible_types(previous_component)):
            error = 'Invalid expression'
            break
        elif component == '(':
            parentheses.append(component)
        elif component == ')':
            if len(parentheses) != 0:
                parentheses.pop()
            else:
                error = 'Invalid expression'
                break
        previous_component = component
    if parentheses:
        error = 'Invalid expression'
    if error:
        print(error)
        return False
    return True


def calculate(postfix):
    stack = deque()
    for component in postfix:
        if typeof(component) == 'number':
            stack.append(int(component))
        elif typeof(component) == 'variable':
            stack.append(get_value(component))
        else:
            b = stack.pop()
            a = stack.pop()
            if component == '+':
                a += b
            if component == '-':
                a -= b
            if component == '*':
                a *= b
            if component == '/':
                a /= b
            if component == '^':
                a **= b
            stack.append(a)
    return int(stack[0])


def m_eval(expression):
    infix = parse(expression)
    if check_syntax(infix):
        print(calculate(infix_to_postfix(simplify_expr(infix))))


def assign(dst, src):
    dst = dst.strip()
    src = src.strip()
    if not dst.isalpha():
        print("Invalid identifier")
        return
    value = get_value(src)
    if isinstance(value, int):
        variables[dst] = value
    else:
        print(value)


if __name__ == '__main__':
    variables = dict()
    while True:
        expr = input().strip()

        if len(expr) == 0:
            continue
        elif expr[0] == '/':
            if run(expr) == 'continue':
                continue
            else:
                break
        elif '=' in expr:
            eq_pos = 0
            for i in range(len(expr)):
                if '=' == expr[i]:
                    eq_pos = i
                    break
            assign(expr[:eq_pos], expr[eq_pos + 1:])
        else:
            m_eval(expr)
