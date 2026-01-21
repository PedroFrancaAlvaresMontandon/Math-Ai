"""
Advanced statistics tool for calculating comprehensive statistical measures.
"""
import json
import statistics
from typing import List
import numpy as np
from langchain_core.tools import tool


def parse_numbers(numbers_str: str) -> List[float]:
    """
    Parses comma-separated numbers into a list of floats.

    Args:
        numbers_str: String of comma-separated numbers

    Returns:
        List of float values

    Raises:
        ValueError: If the input cannot be parsed
    """
    try:
        # Remove whitespace and split by comma
        numbers = [float(x.strip()) for x in numbers_str.split(',') if x.strip()]
        return numbers
    except ValueError as e:
        raise ValueError(f"Formato de número inválido: {str(e)}")


@tool
def statistics_analyzer(numbers: str) -> str:
    """
    Calculates comprehensive statistical measures for a dataset.

    Calculates the following statistics:
    - Mean (average)
    - Median (middle value)
    - Mode (most frequent value)
    - Standard Deviation
    - Variance
    - Minimum and Maximum values
    - Range (max - min)
    - Quartiles (Q1, Q2/Median, Q3)
    - Interquartile Range (IQR)
    - Value count

    Args:
        numbers: Comma-separated numbers as string.
                Examples:
                - '10, 20, 30, 40, 50'
                - '1.5, 2.3, 4.7, 8.9'
                - '100, 200, 150, 175, 225, 180'

    Returns:
        A JSON-formatted string containing all statistical measures.

    Examples:
        >>> statistics_analyzer("10, 20, 30, 40, 50")
        {
          "contagem": 5,
          "media": 30.0,
          "mediana": 30.0,
          "moda": "Sem moda única",
          "desvio_padrao": 14.142,
          "variancia": 200.0,
          "minimo": 10.0,
          "maximo": 50.0,
          "amplitude": 40.0,
          "q1": 20.0,
          "q2": 30.0,
          "q3": 40.0,
          "iqr": 20.0
        }
    """
    try:
        # Parse input
        if not numbers or not numbers.strip():
            return json.dumps({
                "erro": "Entrada vazia fornecida. Por favor, forneça números separados por vírgula."
            }, indent=2, ensure_ascii=False)

        # Parse comma-separated numbers
        try:
            data = parse_numbers(numbers)
        except ValueError as e:
            return json.dumps({
                "erro": f"Formato de entrada inválido: {str(e)}. Por favor, forneça números separados por vírgula como '1, 2, 3, 4, 5'."
            }, indent=2, ensure_ascii=False)

        if not data:
            return json.dumps({
                "erro": "Nenhum número válido encontrado na entrada."
            }, indent=2, ensure_ascii=False)

        if len(data) == 1:
            single_value = data[0]
            return json.dumps({
                "contagem": 1,
                "valor": single_value,
                "nota": "Apenas um valor fornecido. A maioria das medidas estatísticas requer múltiplos valores."
            }, indent=2, ensure_ascii=False)

        # Convert to numpy array for calculations
        np_data = np.array(data)

        # Calculate basic statistics
        mean_val = float(np.mean(np_data))
        median_val = float(np.median(np_data))
        std_dev = float(np.std(np_data, ddof=1))  # Sample standard deviation
        variance = float(np.var(np_data, ddof=1))  # Sample variance
        min_val = float(np.min(np_data))
        max_val = float(np.max(np_data))
        range_val = max_val - min_val

        # Calculate mode
        try:
            mode_val = statistics.mode(data)
            mode_str = str(mode_val)
        except statistics.StatisticsError:
            # No unique mode
            mode_str = "Sem moda única"

        # Calculate quartiles
        q1 = float(np.percentile(np_data, 25))
        q2 = float(np.percentile(np_data, 50))  # Same as median
        q3 = float(np.percentile(np_data, 75))
        iqr = q3 - q1

        # Build results dictionary
        result = {
            "contagem": len(data),
            "media": round(mean_val, 3),
            "mediana": round(median_val, 3),
            "moda": mode_str,
            "desvio_padrao": round(std_dev, 3),
            "variancia": round(variance, 3),
            "minimo": round(min_val, 3),
            "maximo": round(max_val, 3),
            "amplitude": round(range_val, 3),
            "q1": round(q1, 3),
            "q2": round(q2, 3),
            "q3": round(q3, 3),
            "iqr": round(iqr, 3)
        }

        return json.dumps(result, indent=2, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "erro": f"Ocorreu um erro inesperado: {str(e)}"
        }, indent=2, ensure_ascii=False)
