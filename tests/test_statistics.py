"""
Testes unitários para a ferramenta de análise estatística.

Testa cálculos estatísticos, casos extremos e tratamento de erros.
"""
import pytest
import json
from src.tools.statistics import statistics_analyzer


class TestStatisticsNormalDatasets:
    """Testes para datasets normais."""

    def test_simple_dataset(self):
        """
        Testa análise de um dataset simples.

        Dataset: 1, 2, 3, 4, 5
        Média esperada: 3.0
        """
        result = statistics_analyzer("1, 2, 3, 4, 5")
        assert isinstance(result, str)

        # Verifica se é JSON válido
        data = json.loads(result)
        assert isinstance(data, dict)

        # Verifica se não há erro
        assert "erro" not in data

        # Verifica média
        assert "media" in data
        assert data["media"] == 3.0

        # Verifica mediana
        assert "mediana" in data
        assert data["mediana"] == 3.0

    def test_statistics_fields_present(self):
        """
        Verifica se todos os campos estatísticos estão presentes.
        """
        result = statistics_analyzer("10, 20, 30, 40, 50")
        data = json.loads(result)

        expected_fields = [
            "contagem", "media", "mediana", "moda",
            "desvio_padrao", "variancia", "minimo",
            "maximo", "amplitude", "q1", "q2", "q3", "iqr"
        ]

        for field in expected_fields:
            assert field in data, f"Campo '{field}' não encontrado no resultado"

    @pytest.mark.parametrize("numbers,expected_mean", [
        ("1, 2, 3, 4, 5", 3.0),
        ("10, 20, 30, 40, 50", 30.0),
        ("5, 5, 5, 5, 5", 5.0),
        ("0, 0, 0, 0, 0", 0.0),
        ("100, 200, 300", 200.0),
    ])
    def test_mean_calculation(self, numbers, expected_mean):
        """Testa cálculo da média para diferentes datasets."""
        result = statistics_analyzer(numbers)
        data = json.loads(result)
        assert data["media"] == expected_mean

    def test_median_calculation(self):
        """Testa cálculo da mediana."""
        # Dataset ímpar
        result = statistics_analyzer("1, 2, 3, 4, 5")
        data = json.loads(result)
        assert data["mediana"] == 3.0

        # Dataset par
        result = statistics_analyzer("1, 2, 3, 4")
        data = json.loads(result)
        assert data["mediana"] == 2.5

    def test_standard_deviation(self):
        """Testa cálculo do desvio padrão."""
        result = statistics_analyzer("10, 20, 30, 40, 50")
        data = json.loads(result)
        assert "desvio_padrao" in data
        assert data["desvio_padrao"] > 0

    def test_min_max_values(self):
        """Testa valores mínimo e máximo."""
        result = statistics_analyzer("5, 15, 10, 20, 3")
        data = json.loads(result)
        assert data["minimo"] == 3.0
        assert data["maximo"] == 20.0
        assert data["amplitude"] == 17.0

    def test_quartiles(self):
        """Testa cálculo de quartis."""
        result = statistics_analyzer("1, 2, 3, 4, 5, 6, 7, 8, 9, 10")
        data = json.loads(result)

        assert "q1" in data
        assert "q2" in data  # Q2 = mediana
        assert "q3" in data
        assert "iqr" in data

        # Q1 < Q2 < Q3
        assert data["q1"] < data["q2"] < data["q3"]

        # IQR = Q3 - Q1
        assert abs(data["iqr"] - (data["q3"] - data["q1"])) < 0.01


class TestStatisticsEdgeCases:
    """Testes para casos extremos."""

    def test_single_value(self):
        """
        Testa dataset com apenas um valor.

        Deve retornar uma nota informativa.
        """
        result = statistics_analyzer("42")
        data = json.loads(result)

        assert "contagem" in data
        assert data["contagem"] == 1
        assert "valor" in data
        assert data["valor"] == 42.0
        assert "nota" in data

    def test_two_values(self):
        """Testa dataset com apenas dois valores."""
        result = statistics_analyzer("10, 20")
        data = json.loads(result)

        assert data["contagem"] == 2
        assert data["media"] == 15.0
        assert data["mediana"] == 15.0

    def test_identical_values(self):
        """
        Testa dataset com todos os valores idênticos.

        Desvio padrão deve ser 0.
        """
        result = statistics_analyzer("5, 5, 5, 5, 5")
        data = json.loads(result)

        assert data["media"] == 5.0
        assert data["mediana"] == 5.0
        assert data["desvio_padrao"] == 0.0
        assert data["variancia"] == 0.0
        assert data["minimo"] == data["maximo"]
        assert data["amplitude"] == 0.0

    def test_large_dataset(self):
        """Testa dataset grande."""
        numbers = ", ".join([str(i) for i in range(1, 101)])  # 1 a 100
        result = statistics_analyzer(numbers)
        data = json.loads(result)

        assert data["contagem"] == 100
        assert data["media"] == 50.5
        assert data["minimo"] == 1.0
        assert data["maximo"] == 100.0

    def test_negative_numbers(self):
        """Testa dataset com números negativos."""
        result = statistics_analyzer("-10, -5, 0, 5, 10")
        data = json.loads(result)

        assert data["media"] == 0.0
        assert data["minimo"] == -10.0
        assert data["maximo"] == 10.0

    def test_floating_point_numbers(self):
        """Testa dataset com números decimais."""
        result = statistics_analyzer("1.5, 2.3, 3.7, 4.9")
        data = json.loads(result)

        assert "erro" not in data
        assert data["contagem"] == 4
        assert data["minimo"] == 1.5
        assert data["maximo"] == 4.9

    def test_mixed_integers_and_floats(self):
        """Testa dataset com inteiros e decimais misturados."""
        result = statistics_analyzer("1, 2.5, 3, 4.7, 5")
        data = json.loads(result)

        assert "erro" not in data
        assert data["contagem"] == 5


class TestStatisticsErrorHandling:
    """Testes para tratamento de erros."""

    def test_empty_string(self):
        """
        Testa entrada vazia.

        Deve retornar mensagem de erro apropriada.
        """
        result = statistics_analyzer("")
        assert isinstance(result, str)
        data = json.loads(result)
        assert "erro" in data

    def test_whitespace_only(self):
        """Testa entrada com apenas espaços em branco."""
        result = statistics_analyzer("   ")
        data = json.loads(result)
        assert "erro" in data

    def test_invalid_input(self):
        """Testa entrada com texto inválido."""
        result = statistics_analyzer("abc, def, ghi")
        data = json.loads(result)
        assert "erro" in data

    def test_mixed_valid_invalid(self):
        """Testa mistura de números válidos e inválidos."""
        result = statistics_analyzer("1, 2, abc, 4")
        data = json.loads(result)
        assert "erro" in data

    def test_special_characters(self):
        """Testa entrada com caracteres especiais."""
        result = statistics_analyzer("1, @, #, 4")
        data = json.loads(result)
        assert "erro" in data

    @pytest.mark.parametrize("invalid_input", [
        "not a number",
        "one, two, three",
        "1 2 3",  # Sem vírgulas
        "1; 2; 3",  # Separador incorreto
        "1,, 2, 3",  # Vírgulas duplas
    ])
    def test_various_invalid_inputs(self, invalid_input):
        """Testa várias entradas inválidas."""
        result = statistics_analyzer(invalid_input)
        # Deve retornar erro ou processá-las (dependendo da implementação)
        assert isinstance(result, str)
        data = json.loads(result)
        # Pode ter erro ou processar apenas valores válidos
        assert isinstance(data, dict)


class TestStatisticsOutputFormat:
    """Testes para verificar formato de saída."""

    def test_output_is_json(self):
        """Verifica se a saída é JSON válido."""
        result = statistics_analyzer("1, 2, 3, 4, 5")
        assert isinstance(result, str)

        # Deve ser possível fazer parse como JSON
        data = json.loads(result)
        assert isinstance(data, dict)

    def test_output_is_parseable(self):
        """Verifica se a saída pode ser parseada sem erros."""
        result = statistics_analyzer("10, 20, 30")
        try:
            data = json.loads(result)
            assert True
        except json.JSONDecodeError:
            pytest.fail("Output não é JSON válido")

    def test_numeric_values_are_numbers(self):
        """Verifica se valores numéricos no JSON são realmente números."""
        result = statistics_analyzer("1, 2, 3, 4, 5")
        data = json.loads(result)

        numeric_fields = ["media", "mediana", "desvio_padrao", "variancia",
                         "minimo", "maximo", "amplitude", "q1", "q2", "q3", "iqr"]

        for field in numeric_fields:
            if field in data:
                assert isinstance(data[field], (int, float))

    def test_count_is_integer(self):
        """Verifica se contagem é um inteiro."""
        result = statistics_analyzer("1, 2, 3, 4, 5")
        data = json.loads(result)
        assert isinstance(data["contagem"], int)


class TestStatisticsMode:
    """Testes específicos para o cálculo de moda."""

    def test_mode_with_unique_mode(self):
        """Testa dataset com moda única."""
        result = statistics_analyzer("1, 2, 2, 2, 3, 4")
        data = json.loads(result)
        assert "moda" in data
        assert "2" in str(data["moda"])

    def test_mode_without_unique_mode(self):
        """Testa dataset sem moda única."""
        result = statistics_analyzer("1, 2, 3, 4, 5")
        data = json.loads(result)
        assert "moda" in data
        # Quando não há moda única, deve indicar isso
        assert "nica" in str(data["moda"]).lower() or isinstance(data["moda"], str)


class TestStatisticsRounding:
    """Testes para verificar arredondamento de valores."""

    def test_values_are_rounded(self):
        """Verifica se valores são arredondados adequadamente."""
        result = statistics_analyzer("1, 2, 3, 4, 5, 6, 7, 8, 9")
        data = json.loads(result)

        # Valores devem estar arredondados para 3 casas decimais
        for key, value in data.items():
            if isinstance(value, float):
                # Verifica se não tem mais de 3 casas decimais
                decimal_places = len(str(value).split('.')[-1]) if '.' in str(value) else 0
                assert decimal_places <= 3, f"{key} tem muitas casas decimais: {value}"
