"""
Advanced date calculator tool for date and time calculations.
"""
from datetime import datetime, timedelta
from typing import Optional
from langchain_core.tools import tool


def validate_date_format(date_str: str) -> datetime:
    """
    Validates and parses a date string in YYYY-MM-DD format.

    Args:
        date_str: Date string to validate

    Returns:
        Parsed datetime object

    Raises:
        ValueError: If the date format is invalid
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            f"Invalid date format: '{date_str}'. Please use YYYY-MM-DD format (e.g., '2024-01-15')"
        )


@tool
def date_calculator(operation: str, date1: str, date2: Optional[str] = None) -> str:
    """
    Performs various date and time calculations.

    Supported operations:
    1. 'difference' - Calculates days between two dates (requires date1 and date2)
    2. 'add_days' - Adds days to a date (date1=base date, date2=number of days as string)
    3. 'subtract_days' - Subtracts days from a date (date1=base date, date2=number of days as string)
    4. 'age' - Calculates age in years from birth date to today (requires date1 as birth date)
    5. 'day_of_week' - Gets the day name for a specific date (requires date1)

    Args:
        operation: The type of operation to perform.
                  Must be one of: 'difference', 'add_days', 'subtract_days', 'age', 'day_of_week'
        date1: First date in YYYY-MM-DD format, or base date for operations
        date2: Second date in YYYY-MM-DD format (for 'difference'),
              or number of days as string (for 'add_days'/'subtract_days')

    Returns:
        A string with the calculation result in readable format.

    Examples:
        >>> date_calculator("difference", "2024-01-01", "2024-12-31")
        "A diferença entre 2024-01-01 e 2024-12-31 é de 365 dias."

        >>> date_calculator("add_days", "2024-01-01", "30")
        "2024-01-01 mais 30 dias é 2024-01-31."

        >>> date_calculator("subtract_days", "2024-03-15", "45")
        "2024-03-15 menos 45 dias é 2024-01-30."

        >>> date_calculator("age", "1990-03-15")
        "Idade de 1990-03-15 até hoje é 34 anos."

        >>> date_calculator("day_of_week", "2024-01-01")
        "2024-01-01 cai em uma Segunda-feira."
    """
    try:
        # Validate operation
        valid_operations = ['difference', 'add_days', 'subtract_days', 'age', 'day_of_week']
        operation = operation.lower().strip()

        if operation not in valid_operations:
            return (
                f"Erro: Operação inválida '{operation}'. "
                f"Operações suportadas são: {', '.join(valid_operations)}"
            )

        # Validate date1
        if not date1 or not date1.strip():
            return "Erro: parâmetro date1 é obrigatório."

        try:
            dt1 = validate_date_format(date1.strip())
        except ValueError as e:
            return f"Erro em date1: {str(e)}"

        # Process each operation
        if operation == 'difference':
            # Requires both dates
            if not date2 or not date2.strip():
                return "Erro: operação 'difference' requer tanto date1 quanto date2."

            try:
                dt2 = validate_date_format(date2.strip())
            except ValueError as e:
                return f"Erro em date2: {str(e)}"

            # Calculate difference
            difference = abs((dt2 - dt1).days)
            return f"A diferença entre {date1} e {date2} é de {difference} dias."

        elif operation == 'add_days':
            # Requires date1 and number of days in date2
            if not date2 or not date2.strip():
                return "Erro: operação 'add_days' requer date2 como o número de dias a adicionar."

            try:
                days_to_add = int(date2.strip())
            except ValueError:
                return f"Erro: date2 deve ser um inteiro válido (número de dias), recebido '{date2}'."

            result_date = dt1 + timedelta(days=days_to_add)
            result_str = result_date.strftime("%Y-%m-%d")
            return f"{date1} mais {days_to_add} dias é {result_str}."

        elif operation == 'subtract_days':
            # Requires date1 and number of days in date2
            if not date2 or not date2.strip():
                return "Erro: operação 'subtract_days' requer date2 como o número de dias a subtrair."

            try:
                days_to_subtract = int(date2.strip())
            except ValueError:
                return f"Erro: date2 deve ser um inteiro válido (número de dias), recebido '{date2}'."

            result_date = dt1 - timedelta(days=days_to_subtract)
            result_str = result_date.strftime("%Y-%m-%d")
            return f"{date1} menos {days_to_subtract} dias é {result_str}."

        elif operation == 'age':
            # Calculate age from date1 to today
            today = datetime.now()
            age_years = today.year - dt1.year

            # Adjust if birthday hasn't occurred yet this year
            if (today.month, today.day) < (dt1.month, dt1.day):
                age_years -= 1

            if age_years < 0:
                return f"Erro: A data de nascimento {date1} está no futuro."

            return f"Idade de {date1} até hoje é {age_years} anos."

        elif operation == 'day_of_week':
            # Get day of week name
            day_names = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
            day_name = day_names[dt1.weekday()]
            return f"{date1} cai em uma {day_name}."

    except Exception as e:
        return f"Erro: Ocorreu um erro inesperado: {str(e)}"
