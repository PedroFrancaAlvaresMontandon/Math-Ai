"""
Testes unitários para a ferramenta de calculadora de datas.

Testa todas as operações com datas e tratamento de erros.
"""
import pytest
from datetime import datetime
from src.tools.date_calculator import date_calculator


class TestDateCalculatorDifference:
    """Testes para a operação 'difference'."""

    def test_difference_basic(self):
        """
        Testa cálculo básico de diferença entre datas.

        Entre 2024-01-01 e 2024-12-31 há 365 dias (2024 é bissexto).
        """
        result = date_calculator("difference", "2024-01-01", "2024-12-31")
        assert isinstance(result, str)
        assert "365" in result
        assert "dias" in result

    @pytest.mark.parametrize("date1,date2,expected_days", [
        ("2024-01-01", "2024-01-31", "30"),
        ("2024-01-01", "2024-02-01", "31"),
        ("2024-01-15", "2024-01-20", "5"),
        ("2024-06-01", "2024-06-30", "29"),
    ])
    def test_difference_various_dates(self, date1, date2, expected_days):
        """Testa diferença entre várias combinações de datas."""
        result = date_calculator("difference", date1, date2)
        assert expected_days in result
        assert "dias" in result

    def test_difference_same_dates(self):
        """Testa diferença entre datas iguais (deve ser 0)."""
        result = date_calculator("difference", "2024-01-01", "2024-01-01")
        assert "0" in result
        assert "dias" in result

    def test_difference_reversed_dates(self):
        """
        Testa diferença com datas em ordem reversa.

        O resultado deve ser o mesmo (valor absoluto).
        """
        result1 = date_calculator("difference", "2024-01-01", "2024-12-31")
        result2 = date_calculator("difference", "2024-12-31", "2024-01-01")

        # Ambos devem ter o mesmo número de dias
        assert "365" in result1
        assert "365" in result2


class TestDateCalculatorAddDays:
    """Testes para a operação 'add_days'."""

    def test_add_days_basic(self):
        """
        Testa adição de dias a uma data.

        2024-01-01 + 30 dias = 2024-01-31
        """
        result = date_calculator("add_days", "2024-01-01", "30")
        assert isinstance(result, str)
        assert "2024-01-31" in result

    @pytest.mark.parametrize("base_date,days,expected_date", [
        ("2024-01-01", "10", "2024-01-11"),
        ("2024-01-15", "15", "2024-01-30"),
        ("2024-01-31", "1", "2024-02-01"),
        ("2024-12-31", "1", "2025-01-01"),
    ])
    def test_add_days_various(self, base_date, days, expected_date):
        """Testa adição de dias em várias situações."""
        result = date_calculator("add_days", base_date, days)
        assert expected_date in result

    def test_add_zero_days(self):
        """Testa adição de zero dias."""
        result = date_calculator("add_days", "2024-01-15", "0")
        assert "2024-01-15" in result

    def test_add_negative_days(self):
        """
        Testa adição de dias negativos (equivalente a subtração).
        """
        result = date_calculator("add_days", "2024-01-15", "-5")
        assert "2024-01-10" in result


class TestDateCalculatorSubtractDays:
    """Testes para a operação 'subtract_days'."""

    def test_subtract_days_basic(self):
        """
        Testa subtração de dias de uma data.

        2024-12-31 - 15 dias = 2024-12-16
        """
        result = date_calculator("subtract_days", "2024-12-31", "15")
        assert isinstance(result, str)
        assert "2024-12-16" in result

    @pytest.mark.parametrize("base_date,days,expected_date", [
        ("2024-01-15", "5", "2024-01-10"),
        ("2024-02-01", "1", "2024-01-31"),
        ("2024-03-01", "29", "2024-02-01"),  # 2024 é bissexto
        ("2025-01-01", "1", "2024-12-31"),
    ])
    def test_subtract_days_various(self, base_date, days, expected_date):
        """Testa subtração de dias em várias situações."""
        result = date_calculator("subtract_days", base_date, days)
        assert expected_date in result

    def test_subtract_zero_days(self):
        """Testa subtração de zero dias."""
        result = date_calculator("subtract_days", "2024-06-15", "0")
        assert "2024-06-15" in result


class TestDateCalculatorAge:
    """Testes para a operação 'age'."""

    def test_age_calculation(self):
        """
        Testa cálculo de idade.

        Nota: Este teste pode falhar se executado em datas diferentes.
        """
        # Usa uma data de nascimento que garante idade específica
        # Por exemplo, alguém nascido em 1990-01-01
        result = date_calculator("age", "1990-01-01")
        assert isinstance(result, str)
        assert "anos" in result
        # A idade deve estar entre 34 e 35 anos (dependendo do mês atual)
        assert "34" in result or "35" in result

    def test_age_recent_birth(self):
        """Testa idade de pessoa nascida recentemente."""
        # Alguém nascido há 1 ano
        one_year_ago = datetime(datetime.now().year - 1, 1, 1).strftime("%Y-%m-%d")
        result = date_calculator("age", one_year_ago)
        # Deve ter 0 ou 1 ano
        assert "0" in result or "1" in result

    def test_age_future_date_error(self):
        """
        Testa cálculo de idade com data futura.

        Deve retornar erro.
        """
        future_date = "2030-01-01"
        result = date_calculator("age", future_date)
        assert "Erro" in result or "futuro" in result.lower()


class TestDateCalculatorDayOfWeek:
    """Testes para a operação 'day_of_week'."""

    def test_day_of_week_known_dates(self):
        """
        Testa dia da semana para datas conhecidas.

        2024-01-01 foi uma segunda-feira.
        """
        result = date_calculator("day_of_week", "2024-01-01")
        assert isinstance(result, str)
        assert "Segunda-feira" in result or "segunda" in result.lower()

    @pytest.mark.parametrize("date,expected_day", [
        ("2024-01-01", "Segunda"),  # Segunda-feira
        ("2024-12-25", "Quarta"),   # Quarta-feira
        ("2024-07-04", "Quinta"),   # Quinta-feira
    ])
    def test_various_days_of_week(self, date, expected_day):
        """Testa dia da semana para várias datas."""
        result = date_calculator("day_of_week", date)
        assert expected_day.lower() in result.lower()


class TestDateCalculatorErrorHandling:
    """Testes para tratamento de erros."""

    def test_invalid_date_format(self):
        """
        Testa formato de data inválido.

        Deve aceitar apenas YYYY-MM-DD.
        """
        result = date_calculator("difference", "2024/01/01", "2024/12/31")
        assert "Erro" in result

        result = date_calculator("difference", "01-01-2024", "31-12-2024")
        assert "Erro" in result

        result = date_calculator("difference", "2024.01.01", "2024.12.31")
        assert "Erro" in result

    def test_invalid_operation(self):
        """Testa operação inválida."""
        result = date_calculator("unknown_operation", "2024-01-01")
        assert "Erro" in result
        assert "inválida" in result.lower() or "invalid" in result.lower()

    def test_missing_date1(self):
        """Testa quando date1 está ausente."""
        result = date_calculator("difference", "", "2024-12-31")
        assert "Erro" in result

    def test_missing_date2_for_difference(self):
        """
        Testa quando date2 está ausente para operação 'difference'.
        """
        result = date_calculator("difference", "2024-01-01", None)
        assert "Erro" in result

    def test_invalid_date_values(self):
        """Testa valores de data inválidos."""
        # Mês inválido
        result = date_calculator("difference", "2024-13-01", "2024-12-31")
        assert "Erro" in result

        # Dia inválido
        result = date_calculator("difference", "2024-01-32", "2024-12-31")
        assert "Erro" in result

    def test_non_numeric_days_for_add(self):
        """Testa valor não numérico para número de dias."""
        result = date_calculator("add_days", "2024-01-01", "abc")
        assert "Erro" in result

    @pytest.mark.parametrize("operation,date1,date2", [
        ("difference", "invalid", "2024-12-31"),
        ("add_days", "2024-01-01", "not_a_number"),
        ("subtract_days", "2024-01-01", "xyz"),
        ("age", "not-a-date", None),
        ("day_of_week", "2024-99-99", None),
    ])
    def test_various_error_cases(self, operation, date1, date2):
        """Testa vários casos de erro."""
        result = date_calculator(operation, date1, date2)
        assert "Erro" in result


class TestDateCalculatorOutputFormat:
    """Testes para verificar formato de saída."""

    def test_output_is_string(self):
        """Verifica se todas as operações retornam string."""
        result = date_calculator("difference", "2024-01-01", "2024-12-31")
        assert isinstance(result, str)

    def test_output_is_human_readable(self):
        """Verifica se a saída é legível por humanos."""
        result = date_calculator("difference", "2024-01-01", "2024-12-31")
        assert isinstance(result, str)
        # Deve conter palavras em português
        assert any(word in result.lower() for word in ["dias", "diferença", "entre"])

    @pytest.mark.parametrize("operation", [
        "difference",
        "add_days",
        "subtract_days",
        "age",
        "day_of_week",
    ])
    def test_all_operations_return_string(self, operation):
        """Verifica que todas as operações retornam string."""
        if operation == "difference":
            result = date_calculator(operation, "2024-01-01", "2024-12-31")
        elif operation in ["add_days", "subtract_days"]:
            result = date_calculator(operation, "2024-01-01", "10")
        else:
            result = date_calculator(operation, "2024-01-01")

        assert isinstance(result, str)


class TestDateCalculatorLeapYears:
    """Testes específicos para anos bissextos."""

    def test_leap_year_february(self):
        """
        Testa operações em ano bissexto (2024).

        Fevereiro de 2024 tem 29 dias.
        """
        # Diferença em fevereiro de ano bissexto
        result = date_calculator("difference", "2024-02-01", "2024-02-29")
        assert "28" in result

        # Adicionar dias passando por fevereiro bissexto
        result = date_calculator("add_days", "2024-02-28", "1")
        assert "2024-02-29" in result

    def test_non_leap_year_february(self):
        """
        Testa operações em ano não bissexto (2023).

        Fevereiro de 2023 tem 28 dias.
        """
        result = date_calculator("difference", "2023-02-01", "2023-03-01")
        assert "28" in result


class TestDateCalculatorCaseSensitivity:
    """Testes para verificar se as operações são case-insensitive."""

    @pytest.mark.parametrize("operation", [
        "DIFFERENCE",
        "Difference",
        "DiFfErEnCe",
        "ADD_DAYS",
        "add_DAYS",
    ])
    def test_case_insensitive_operations(self, operation):
        """Verifica se operações são case-insensitive."""
        if "diff" in operation.lower():
            result = date_calculator(operation, "2024-01-01", "2024-01-10")
        else:
            result = date_calculator(operation, "2024-01-01", "10")

        # Não deve retornar erro de operação inválida
        assert isinstance(result, str)
        # Se tiver "Erro" e "inválida", então não é case-insensitive
        if "Erro" in result and "inválida" in result.lower():
            pytest.fail(f"Operação {operation} não é case-insensitive")
