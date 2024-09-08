from typing import List, Union, Dict, Any

# Define types for clarity
Text = str
Operator = str
Parenthesis = str

class Token:
    def __init__(self, token_type: str, value: Union[Text, Operator, Parenthesis, float], token: str = None, number_type: str = None):
        self.type = token_type
        self.token = token
        self.value = value
        self.number_type = number_type

NestedToken = Union[Token, List['NestedToken']]

def is_operator(token: Token) -> bool:
    # Check if the token is an operator.
    return token.type == 'operator'

def is_parenthesis(token: Token) -> bool:
    # vCheck if the token is a parenthesis.
    return token.type == 'parenthesis'

def is_numeric(token: str) -> bool:
    # Check if the token is numeric.
    try:
        float(token)
        return True
    except ValueError:
        return False
      
def is_text(token: str) -> bool:
    # Check if the token is a text word (not numeric).
    try:
        float(token)
        return False
    except ValueError:
        return True

def evaluate_expression(tokens: List[Token]) -> float:
    # Calculate the logic string considering the precedence of the operators and the parenthesis.
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    def apply_operator(a: float, b: float, operator: Operator) -> float:
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            return a / b
        else:
            return 0

    value_stack = []
    operator_stack = []

    for token in tokens:
        if token.type == 'text':
            value_stack.append(token.value)
        elif token.type in ('number', 'variable'):
            if token.number_type == 'percentage':
                token.value = float(token.value) / 100
            value_stack.append(float(token.value))
        elif is_parenthesis(token) and token.value == '(':
            operator_stack.append(token)
        elif is_parenthesis(token) and token.value == ')':
            while operator_stack and operator_stack[-1].type != 'parenthesis':
                operator_token = operator_stack.pop()
                operator = operator_token.value
                b = value_stack.pop()
                a = value_stack.pop()
                value_stack.append(apply_operator(a, b, operator))
            if not operator_stack or operator_stack.pop().value != '(':
                raise ValueError('Mismatched parentheses')
        elif is_operator(token):
            while (operator_stack and is_operator(operator_stack[-1]) and 
                   precedence[token.value] <= precedence[operator_stack[-1].value]):
                operator = operator_stack.pop().value
                b = value_stack.pop()
                a = value_stack.pop()
                value_stack.append(apply_operator(a, b, operator))
            operator_stack.append(token)

    while operator_stack:
        operator = operator_stack.pop().value
        b = value_stack.pop()
        a = value_stack.pop()
        value_stack.append(apply_operator(a, b, operator))

    return value
      # Return the result or 0 if NaN
    return value_stack[0] if not is_numeric(str(value_stack[0])) else 0

def tokenize(obj: Dict[str, Any]) -> List[Token]:
    # Create an array of tokens from the logic string.
    tokens = []
    current_token = ''

    for char in obj['request']:
        if char == ' ':
            continue
        if char in '+-*/()':
            if current_token:
                if is_text(current_token):
                  tokens.append(Token(
                      token_type='text',
                      token=current_token,
                      value=obj[current_token],
                      text_type=obj.get(f"{current_token}_text_type")
                  ))
                elif is_numeric(current_token):
                    tokens.append(Token(token_type='number', value=float(current_token)))
                else:
                    tokens.append(Token(
                        token_type='variable',
                        token=current_token,
                        value=float(obj[current_token]),
                        number_type=obj.get(f"{current_token}_number_type")
                    ))
                current_token = ''
            tokens.append(Token(token_type='parenthesis' if char in '()' else 'operator', value=char))
        else:
            current_token += char

    if current_token:
        if is_text(current_token):
          tokens.append(Token(
              token_type='text',
              token=current_token,
              value=obj[current_token],
              text_type=obj.get(f"{current_token}_text_type")
          ))
        elif is_numeric(current_token):
            tokens.append(Token(token_type='number', value=float(current_token)))
        else:
            tokens.append(Token(
                token_type='variable',
                token=current_token,
                value=float(obj[current_token]),
                number_type=obj.get(f"{current_token}_number_type")
            ))

    return tokens

def build_nested_expression(tokens: List[Token]) -> List[NestedToken]:
    # Convert a list of tokens into a nested token structure.
    copied_tokens = tokens[:]
    opening_braces = sum(1 for token in copied_tokens if token.type == 'parenthesis' and token.value == '(')
    closing_braces = sum(1 for token in copied_tokens if token.type == 'parenthesis' and token.value == ')')

    while opening_braces < closing_braces:
        copied_tokens.insert(0, Token(token_type='parenthesis', value='('))
        opening_braces += 1
    while closing_braces < opening_braces:
        copied_tokens.append(Token(token_type='parenthesis', value=')'))
        closing_braces += 1

    nested_tokens = []
    i = 0

    while i < len(copied_tokens):
        token = copied_tokens[i]
        if token.type != 'parenthesis':
            nested_tokens.append(token)
        elif token.value == ')':
            continue
        else:
            closing_parenthesis_index = i
            parenthesis_count = 0
            while closing_parenthesis_index < len(copied_tokens):
                temp_token = copied_tokens[closing_parenthesis_index]
                if temp_token.type == 'parenthesis' and temp_token.value == '(':
                    parenthesis_count += 1
                elif temp_token.type == 'parenthesis' and temp_token.value == ')':
                    parenthesis_count -= 1
                if parenthesis_count == 0:
                    break
                closing_parenthesis_index += 1

            sub_calculation = copied_tokens[i + 1:closing_parenthesis_index]
            nested_tokens.append(build_nested_expression(sub_calculation))
            i = closing_parenthesis_index

        i += 1

    return nested_tokens

def validate_expression(tokens: List[NestedToken]) -> bool:
    # Check if the nested tokens represent a valid calculation.
    if len(tokens) % 2 == 0:
        return False

    for i in range(len(tokens)):
        token = tokens[i]
        if i % 2 == 0 and not isinstance(token, list) and token.type == 'operator':
            return False
        elif i % 2 == 1 and (isinstance(token, list) or token.type != 'operator'):
            return False

        if isinstance(token, list) and not validate_expression(token):
            return False

    return True

def flatten_expression(tokens: List[NestedToken]) -> List[Token]:
    # Flatten a nested token structure into a list of tokens.
    flattened_tokens = []

    for token in tokens:
        if isinstance(token, list):
            flattened_tokens.append(Token(token_type='parenthesis', value='('))
            flattened_tokens.extend(flatten_expression(token))
            flattened_tokens.append(Token(token_type='parenthesis', value=')'))
        else:
            flattened_tokens.append(token)

    return flattened_tokens

def remove_text_variable(tokens: List[NestedToken], variable: str) -> List[NestedToken]:
    # Remove a variable from a nested token structure.
    new_tokens = tokens[:]

    for i in range(len(new_tokens) - 1, -1, -2):
        token = new_tokens[i]
        if isinstance(token, list):
            new_tokens[i] = remove_text_variable(token, variable)
            token = new_tokens[i]

        if (isinstance(token, list) and len(token) == 0) or (not isinstance(token, list) and token.type == 'number' and token.token == variable):
            if i == 0:
                new_tokens = new_tokens[2:]
            else:
                new_tokens = new_tokens[:i - 1] + new_tokens[i + 1:]

    return new_tokens

def remove_variable(tokens: List[Token], variable: str) -> List[Token]:
    # Remove a variable from the tokens.
    nested_calculation = build_nested_expression(tokens)
    if not validate_expression(nested_calculation):
        return tokens

    nested_calculation = remove_text_variable(nested_calculation, variable)
    return flatten_expression(nested_calculation)

def use_tokenization():
    #Provide access to the tokenization functions.#
    return {
        'tokenize': tokenize,
        'calculate': calculate,
        'remove_variable': remove_variable,
    }
