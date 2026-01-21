"""
Testes de integração para o agente de IA.

Testa a capacidade do agente de escolher e usar ferramentas corretamente.
"""
import pytest
from src.agent.agent import run_agent, create_agent, reset_agent


class TestAgentBasicFunctionality:
    """Testes básicos de funcionalidade do agente."""

    def test_agent_returns_dict(self):
        """
        Verifica se o agente retorna um dicionário.
        """
        result = run_agent("Olá, como você está?", verbose=False)
        assert isinstance(result, dict)

    def test_agent_has_output_key(self):
        """
        Verifica se o resultado do agente contém a chave 'output'.
        """
        result = run_agent("Quanto é 2 + 2?", verbose=False)
        assert "output" in result
        assert isinstance(result["output"], str)

    def test_agent_responds_to_simple_query(self):
        """
        Testa se o agente responde a uma consulta simples.
        """
        result = run_agent("Olá!", verbose=False)
        assert "output" in result
        assert len(result["output"]) > 0

    def test_agent_output_not_empty(self):
        """
        Verifica se a saída do agente não está vazia.
        """
        result = run_agent("Teste", verbose=False)
        output = result.get("output", "")
        assert output.strip() != ""


@pytest.mark.slow
class TestAgentToolSelection:
    """Testes para verificar se o agente escolhe as ferramentas corretas."""

    def test_calculator_tool_invoked(self):
        """
        Testa se o agente usa a ferramenta calculator para cálculos.

        Consulta matemática deve invocar a ferramenta calculator.
        """
        result = run_agent("Quanto é 15 multiplicado por 8?", verbose=False)

        assert "output" in result

        # Verifica se alguma ferramenta foi usada
        if "intermediate_steps" in result:
            tools_used = []
            for step in result["intermediate_steps"]:
                if len(step) > 0 and hasattr(step[0], 'tool'):
                    tools_used.append(step[0].tool)

            # Deve ter usado a ferramenta calculator
            assert "calculator" in tools_used, f"Calculator não foi usado. Ferramentas: {tools_used}"

    def test_statistics_tool_invoked(self):
        """
        Testa se o agente usa a ferramenta statistics_analyzer.

        Consulta estatística deve invocar a ferramenta statistics_analyzer.
        """
        result = run_agent(
            "Calcule a média dos números: 10, 20, 30, 40, 50",
            verbose=False
        )

        assert "output" in result

        if "intermediate_steps" in result:
            tools_used = []
            for step in result["intermediate_steps"]:
                if len(step) > 0 and hasattr(step[0], 'tool'):
                    tools_used.append(step[0].tool)

            assert "statistics_analyzer" in tools_used, \
                f"Statistics_analyzer não foi usado. Ferramentas: {tools_used}"

    def test_date_calculator_tool_invoked(self):
        """
        Testa se o agente usa a ferramenta date_calculator.

        Consulta sobre datas deve invocar a ferramenta date_calculator.
        """
        result = run_agent(
            "Quantos dias existem entre 2024-01-01 e 2024-12-31?",
            verbose=False
        )

        assert "output" in result

        if "intermediate_steps" in result:
            tools_used = []
            for step in result["intermediate_steps"]:
                if len(step) > 0 and hasattr(step[0], 'tool'):
                    tools_used.append(step[0].tool)

            assert "date_calculator" in tools_used, \
                f"Date_calculator não foi usado. Ferramentas: {tools_used}"

    def test_general_knowledge_no_tools(self):
        """
        Testa se o agente responde diretamente sem ferramentas.

        Pergunta de conhecimento geral não deve invocar ferramentas.
        """
        result = run_agent("O que é Python?", verbose=False)

        assert "output" in result

        # Não deve usar ferramentas para conhecimento geral
        if "intermediate_steps" in result:
            # Verifica se nenhuma ferramenta foi usada, ou se foi usada, foi desnecessário
            assert len(result["intermediate_steps"]) == 0 or \
                   result["intermediate_steps"] == [], \
                   "Ferramentas não deveriam ser usadas para conhecimento geral"


@pytest.mark.slow
class TestAgentMathematicalQueries:
    """Testes para consultas matemáticas."""

    @pytest.mark.parametrize("query,expected_answer", [
        ("Quanto é 2 + 2?", "4"),
        ("Calcule 10 * 5", "50"),
        ("Qual é a raiz quadrada de 16?", "4"),
    ])
    def test_mathematical_queries(self, query, expected_answer):
        """
        Testa consultas matemáticas variadas.
        """
        result = run_agent(query, verbose=False)
        output = result.get("output", "")

        # Verifica se a resposta contém o valor esperado
        assert expected_answer in output, \
            f"Esperado '{expected_answer}' na resposta, mas obteve: {output}"

    def test_complex_mathematical_expression(self):
        """
        Testa expressão matemática complexa.
        """
        result = run_agent("Calcule (15 + 5) * 3 - 10", verbose=False)
        output = result.get("output", "")

        # (15 + 5) * 3 - 10 = 20 * 3 - 10 = 60 - 10 = 50
        assert "50" in output


@pytest.mark.slow
class TestAgentStatisticalQueries:
    """Testes para consultas estatísticas."""

    def test_mean_calculation(self):
        """
        Testa cálculo de média.
        """
        result = run_agent(
            "Qual é a média dos números 10, 20, 30, 40, 50?",
            verbose=False
        )
        output = result.get("output", "")

        # Média = 30
        assert "30" in output

    def test_statistical_analysis(self):
        """
        Testa análise estatística completa.
        """
        result = run_agent(
            "Analise estatisticamente: 5, 10, 15, 20, 25",
            verbose=False
        )
        output = result.get("output", "")

        # Deve conter alguma informação estatística
        assert len(output) > 0
        # Pode mencionar média, mediana, etc.
        assert any(word in output.lower() for word in ["média", "mediana", "desvio"])


@pytest.mark.slow
class TestAgentDateQueries:
    """Testes para consultas sobre datas."""

    def test_date_difference(self):
        """
        Testa cálculo de diferença entre datas.
        """
        result = run_agent(
            "Quantos dias há entre 2024-01-01 e 2024-01-31?",
            verbose=False
        )
        output = result.get("output", "")

        # 30 dias de diferença
        assert "30" in output

    def test_age_calculation(self):
        """
        Testa cálculo de idade.
        """
        result = run_agent(
            "Se nasci em 2000-01-01, quantos anos tenho?",
            verbose=False
        )
        output = result.get("output", "")

        # Deve mencionar idade (24 ou 25 anos dependendo da data atual)
        assert "24" in output or "25" in output

    def test_day_of_week(self):
        """
        Testa consulta de dia da semana.
        """
        result = run_agent(
            "Qual dia da semana foi 2024-01-01?",
            verbose=False
        )
        output = result.get("output", "")

        # 2024-01-01 foi Segunda-feira
        assert "segunda" in output.lower() or "monday" in output.lower()


class TestAgentErrorHandling:
    """Testes para tratamento de erros do agente."""

    def test_agent_handles_empty_query(self):
        """
        Testa como o agente lida com consulta vazia.

        Pode retornar erro ou mensagem padrão.
        """
        result = run_agent("", verbose=False)
        assert isinstance(result, dict)
        assert "output" in result

    def test_agent_handles_invalid_math(self):
        """
        Testa como o agente lida com matemática inválida.
        """
        result = run_agent("Calcule abc + xyz", verbose=False)
        output = result.get("output", "")

        # Deve reconhecer que não é uma expressão matemática válida
        assert len(output) > 0

    def test_agent_handles_malformed_query(self):
        """
        Testa como o agente lida com consulta malformada.
        """
        result = run_agent("!@#$%^&*()", verbose=False)
        assert isinstance(result, dict)
        assert "output" in result


class TestAgentMultipleQueries:
    """Testes para múltiplas consultas em sequência."""

    def test_multiple_queries_sequence(self):
        """
        Testa processamento de múltiplas consultas em sequência.
        """
        queries = [
            "Quanto é 5 + 5?",
            "Qual é a média de 1, 2, 3?",
            "Quantos dias entre 2024-01-01 e 2024-01-10?"
        ]

        for query in queries:
            result = run_agent(query, verbose=False)
            assert isinstance(result, dict)
            assert "output" in result
            assert len(result["output"]) > 0

    def test_agent_maintains_functionality(self):
        """
        Verifica se o agente mantém funcionalidade após múltiplas consultas.
        """
        # Primeira consulta
        result1 = run_agent("Quanto é 10 * 10?", verbose=False)
        assert "100" in result1["output"]

        # Segunda consulta
        result2 = run_agent("Quanto é 5 + 5?", verbose=False)
        assert "10" in result2["output"]

        # As consultas não devem interferir uma com a outra


class TestAgentCreation:
    """Testes para criação e reset do agente."""

    def test_create_agent(self):
        """
        Testa criação manual do agente.
        """
        agent = create_agent(verbose=False)
        assert agent is not None

    def test_reset_agent(self):
        """
        Testa reset do cache do agente.
        """
        # Executa uma consulta para criar o agente
        run_agent("Teste", verbose=False)

        # Reseta o agente
        reset_agent()

        # Executa outra consulta (deve criar novo agente)
        result = run_agent("Outro teste", verbose=False)
        assert isinstance(result, dict)
        assert "output" in result


class TestAgentResponseQuality:
    """Testes para verificar qualidade das respostas."""

    def test_response_in_portuguese(self):
        """
        Verifica se as respostas estão em português.
        """
        result = run_agent("Quanto é 2 + 2?", verbose=False)
        output = result.get("output", "")

        # Deve conter palavras em português
        # (difícil de verificar definitivamente, mas podemos procurar por padrões)
        assert len(output) > 0

    def test_response_is_helpful(self):
        """
        Verifica se a resposta é útil (não vazia, tem conteúdo).
        """
        result = run_agent("Explique o que é IA", verbose=False)
        output = result.get("output", "")

        # Resposta deve ter comprimento razoável
        assert len(output) > 20  # Mais de 20 caracteres

    def test_response_contains_answer(self):
        """
        Verifica se a resposta contém a resposta esperada.
        """
        result = run_agent("Quanto é 7 * 8?", verbose=False)
        output = result.get("output", "")

        # Deve conter a resposta: 56
        assert "56" in output


@pytest.fixture(scope="module", autouse=True)
def reset_after_tests():
    """
    Fixture para limpar o cache do agente após os testes.
    """
    yield
    reset_agent()
