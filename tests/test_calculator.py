"""
Testes unitários para a ferramenta de calculadora.

Testa operações básicas, funções avançadas e tratamento de erros.
"""
import pytest
from src.tools.calculator import calculator


class TestCalculatorBasicOperations:
    """Testes para operações básicas da calculadora."""

    @pytest.mark.parametrize("expression,expected", [
        ("2 + 2", "4"),
        ("10 - 3", "7"),
        ("5 * 6", "30"),
        ("20 / 4", "5"),
        ("100 + 50", "150"),
        ("1000 - 999", "1"),
        ("12 * 12", "144"),
        ("100 / 5", "20"),
    ])
    def test_basic_arithmetic(self, expression, expected):
        """
        Testa operações aritméticas básicas.

        Verifica se adição, subtração, multiplicação e divisão
        retornam os resultados corretos.
        """
        result = calculator(expression)
        assert "Resultado:" in result
        assert expected in result

    def test_addition(self):
        """Testa adição simples."""
        result = calculator("2 + 2")
        assert isinstance(result, str)
        assert "4" in result

    def test_subtraction(self):
        """Testa subtração simples."""
        result = calculator("10 - 3")
        assert isinstance(result, str)
        assert "7" in result

    def test_multiplication(self):
        """Testa multiplicação simples."""
        result = calculator("5 * 6")
        assert isinstance(result, str)
        assert "30" in result

    def test_division(self):
        """Testa divisão simples."""
        result = calculator("20 / 4")
        assert isinstance(result, str)
        assert "5" in result


class TestCalculatorAdvancedOperations:
    """Testes para operações avançadas da calculadora."""

    @pytest.mark.parametrize("expression,expected_in_result", [
        ("2 ** 8", "256"),
        ("sqrt(16)", "4"),
        ("sqrt(25)", "5"),
        ("sqrt(144)", "12"),
        ("pow(2, 3)", "8"),
        ("pow(5, 2)", "25"),
        ("abs(-10)", "10"),
        ("abs(15)", "15"),
    ])
    def test_advanced_functions(self, expression, expected_in_result):
        """
        Testa funções matemáticas avançadas.

        Verifica potência, raiz quadrada, pow(), abs(), etc.
        """
        result = calculator(expression)
        assert isinstance(result, str)
        assert "Resultado:" in result
        assert expected_in_result in result

    def test_power_operation(self):
        """Testa operação de potência."""
        result = calculator("2 ** 8")
        assert "256" in result

    def test_sqrt_function(self):
        """Testa função raiz quadrada."""
        result = calculator("sqrt(16)")
        assert "4" in result

    def test_complex_expression(self):
        """Testa expressão matemática complexa."""
        result = calculator("sqrt(25) + 10 * 2")
        assert "Resultado:" in result
        assert "25" in result

    @pytest.mark.parametrize("expression,expected_contains", [
        ("(10 + 5) * 2", "30"),
        ("100 / (2 + 3)", "20"),
        ("(5 + 3) * (4 - 1)", "24"),
        ("sqrt(9) + sqrt(16)", "7"),
    ])
    def test_complex_expressions(self, expression, expected_contains):
        """
        Testa expressões complexas com parênteses e múltiplas operações.
        """
        result = calculator(expression)
        assert isinstance(result, str)
        assert expected_contains in result

    def test_trigonometric_functions(self):
        """Testa funções trigonométricas."""
        # sin(0) = 0
        result = calculator("sin(0)")
        assert "Resultado:" in result
        assert "0" in result

        # cos(0) = 1
        result = calculator("cos(0)")
        assert "1" in result

    def test_logarithmic_functions(self):
        """Testa funções logarítmicas."""
        result = calculator("log10(100)")
        assert "Resultado:" in result
        assert "2" in result

    def test_exponential_function(self):
        """Testa função exponencial."""
        result = calculator("exp(0)")
        assert "Resultado:" in result
        assert "1" in result

    def test_floor_and_ceil(self):
        """Testa funções floor e ceil."""
        result = calculator("floor(3.7)")
        assert "3" in result

        result = calculator("ceil(3.2)")
        assert "4" in result


class TestCalculatorErrorHandling:
    """Testes para tratamento de erros da calculadora."""

    def test_division_by_zero(self):
        """
        Testa divisão por zero.

        Deve retornar mensagem de erro apropriada sem crashar.
        """
        result = calculator("10 / 0")
        assert isinstance(result, str)
        assert "Erro" in result
        assert "zero" in result.lower()

    def test_invalid_expression(self):
        """Testa expressão inválida."""
        result = calculator("invalid math")
        assert isinstance(result, str)
        assert "Erro" in result

    def test_empty_expression(self):
        """Testa expressão vazia."""
        result = calculator("")
        assert isinstance(result, str)
        assert "Erro" in result

    def test_invalid_syntax(self):
        """Testa sintaxe inválida."""
        result = calculator("2 + + 2")
        assert isinstance(result, str)
        assert "Erro" in result

    @pytest.mark.parametrize("invalid_expr", [
        "2 +",
        "* 5",
        "10 /",
        "((2 + 3)",
        "2 + 3)",
    ])
    def test_malformed_expressions(self, invalid_expr):
        """Testa expressões malformadas."""
        result = calculator(invalid_expr)
        assert isinstance(result, str)
        assert "Erro" in result

    def test_unsupported_function(self):
        """Testa função não suportada."""
        result = calculator("unsupported_func(10)")
        assert isinstance(result, str)
        assert "Erro" in result


class TestCalculatorReturnTypes:
    """Testes para verificar tipos de retorno da calculadora."""

    def test_returns_string(self):
        """Verifica se a calculadora sempre retorna string."""
        result = calculator("2 + 2")
        assert isinstance(result, str)

    def test_result_format(self):
        """Verifica formato da resposta de sucesso."""
        result = calculator("5 * 5")
        assert isinstance(result, str)
        assert "Resultado:" in result or "Erro:" in result

    @pytest.mark.parametrize("expression", [
        "1 + 1",
        "sqrt(4)",
        "10 * 10",
        "100 / 10",
    ])
    def test_all_operations_return_string(self, expression):
        """Verifica que todas as operações retornam string."""
        result = calculator(expression)
        assert isinstance(result, str)


class TestCalculatorEdgeCases:
    """Testes para casos extremos da calculadora."""

    def test_very_large_numbers(self):
        """Testa cálculos com números muito grandes."""
        result = calculator("999999 + 1")
        assert "1000000" in result

    def test_very_small_numbers(self):
        """Testa cálculos com números muito pequenos."""
        result = calculator("0.001 + 0.002")
        assert "Resultado:" in result

    def test_negative_numbers(self):
        """Testa cálculos com números negativos."""
        result = calculator("-5 + 10")
        assert "5" in result

        result = calculator("-10 * 2")
        assert "-20" in result

    def test_floating_point_precision(self):
        """Testa precisão de ponto flutuante."""
        result = calculator("0.1 + 0.2")
        assert "Resultado:" in result
        # Devido à precisão de ponto flutuante, apenas verifica que retorna um resultado
        assert "0.3" in result or "0.30000" in result

    def test_nested_operations(self):
        """Testa operações aninhadas complexas."""
        result = calculator("((2 + 3) * (4 + 1)) / 5")
        assert "Resultado:" in result
        assert "5" in result

    def test_constants(self):
        """Testa uso de constantes matemáticas."""
        # pi
        result = calculator("pi")
        assert "Resultado:" in result
        assert "3.14" in result

        # e
        result = calculator("e")
        assert "Resultado:" in result
        assert "2.7" in result
