"""
Advanced calculator tool for mathematical operations.
"""
import ast
import math
import operator
from typing import Union
from langchain_core.tools import tool


# Supported operators
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Supported mathematical functions
MATH_FUNCTIONS = {
    'sqrt': math.sqrt,
    'pow': pow,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,
    'log10': math.log10,
    'exp': math.exp,
    'abs': abs,
    'ceil': math.ceil,
    'floor': math.floor,
    'pi': math.pi,
    'e': math.e,
}


def safe_eval(node: ast.AST) -> float:
    """
    Safely evaluates an AST (Abstract Syntax Tree) node.

    Args:
        node: AST node to evaluate

    Returns:
        Evaluated result as float

    Raises:
        ValueError: If the expression contains unsupported operations
        ZeroDivisionError: If division by zero is attempted
    """
    if isinstance(node, ast.Constant):
        return float(node.value)

    elif isinstance(node, ast.Name):
        if node.id in MATH_FUNCTIONS:
            return MATH_FUNCTIONS[node.id]
        raise ValueError(f"Unsupported constant: {node.id}")

    elif isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op = OPERATORS.get(type(node.op))

        if op is None:
            raise ValueError(f"Unsupported operation: {type(node.op).__name__}")

        if isinstance(node.op, ast.Div) and right == 0:
            raise ZeroDivisionError("Division by zero is not allowed")

        return op(left, right)

    elif isinstance(node, ast.UnaryOp):
        operand = safe_eval(node.operand)
        op = OPERATORS.get(type(node.op))

        if op is None:
            raise ValueError(f"Unsupported unary operation: {type(node.op).__name__}")

        return op(operand)

    elif isinstance(node, ast.Call):
        func_name = node.func.id if isinstance(node.func, ast.Name) else None

        if func_name not in MATH_FUNCTIONS:
            raise ValueError(f"Unsupported function: {func_name}")

        func = MATH_FUNCTIONS[func_name]
        args = [safe_eval(arg) for arg in node.args]

        try:
            return float(func(*args))
        except Exception as e:
            raise ValueError(f"Error calling {func_name}: {str(e)}")

    elif isinstance(node, ast.Expression):
        return safe_eval(node.body)

    else:
        raise ValueError(f"Unsupported expression type: {type(node).__name__}")


@tool
def calculator(expression: str) -> str:
    """
    Evaluates mathematical expressions including basic operations and common mathematical functions.

    Supports:
    - Basic operations: +, -, *, /, ** (power)
    - Mathematical functions: sqrt(), pow(), sin(), cos(), tan(), log(), log10(), exp(), abs(), ceil(), floor()
    - Constants: pi, e

    Args:
        expression: The mathematical expression to evaluate.
                   Examples:
                   - '2 + 2'
                   - 'sqrt(16)'
                   - 'pow(2, 8)'
                   - '45 * 23 + 17'
                   - 'sin(pi / 2)'
                   - '(10 + 5) * 3 / 2'

    Returns:
        A string containing the calculated result or an error message.

    Examples:
        >>> calculator("2 + 2")
        "Resultado: 4"
        >>> calculator("sqrt(16)")
        "Resultado: 4"
        >>> calculator("pow(2, 8)")
        "Resultado: 256"
        >>> calculator("sin(0)")
        "Resultado: 0"
        >>> calculator("10 / 0")
        "Erro: Divisão por zero não é permitida"
    """
    try:
        # Remove whitespace
        expression = expression.strip()

        if not expression:
            return "Erro: Expressão vazia fornecida"

        # Parse the expression into an AST
        try:
            tree = ast.parse(expression, mode='eval')
        except SyntaxError as e:
            return f"Erro: Sintaxe inválida na expressão: {str(e)}"

        # Safely evaluate the AST
        result = safe_eval(tree)

        # Format the result
        if isinstance(result, float):
            # Remove unnecessary decimal points for integers
            if result.is_integer():
                return f"Resultado: {int(result)}"
            else:
                return f"Resultado: {result}"
        else:
            return f"Resultado: {result}"

    except ZeroDivisionError as e:
        return f"Erro: {str(e)}"
    except ValueError as e:
        return f"Erro: {str(e)}"
    except Exception as e:
        return f"Erro: Ocorreu um erro inesperado: {str(e)}"
