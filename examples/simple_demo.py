"""
Script de demonstração simples do Assistente de IA.

Este script executa uma série de consultas predefinidas para demonstrar
as capacidades do assistente e suas diferentes ferramentas.
"""
import time
from typing import List, Dict

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from src.agent.agent import run_agent


console = Console()


# Queries de demonstração organizadas por categoria
DEMO_QUERIES: List[Dict[str, str]] = [
    {
        "category": "🧮 Calculadora",
        "query": "Quanto é 128 vezes 46?",
        "expected_tool": "calculator"
    },
    {
        "category": "🧮 Calculadora",
        "query": "Qual é a raiz quadrada de 2025?",
        "expected_tool": "calculator"
    },
    {
        "category": "🧮 Calculadora",
        "query": "Calcule: (15 + 25) * 3 - 10",
        "expected_tool": "calculator"
    },
    {
        "category": "📊 Estatística",
        "query": "Calcule a média e o desvio padrão desses números: 10, 20, 30, 40, 50",
        "expected_tool": "statistics_analyzer"
    },
    {
        "category": "📊 Estatística",
        "query": "Qual é a mediana de: 15, 23, 8, 42, 16, 31, 29?",
        "expected_tool": "statistics_analyzer"
    },
    {
        "category": "📊 Estatística",
        "query": "Analise estatisticamente: 100, 200, 150, 175, 225, 180",
        "expected_tool": "statistics_analyzer"
    },
    {
        "category": "📅 Datas",
        "query": "Quantos dias existem entre 2024-01-01 e 2024-12-31?",
        "expected_tool": "date_calculator"
    },
    {
        "category": "📅 Datas",
        "query": "Se nasci em 1990-03-15, quantos anos tenho?",
        "expected_tool": "date_calculator"
    },
    {
        "category": "📅 Datas",
        "query": "Qual dia da semana foi 2024-01-01?",
        "expected_tool": "date_calculator"
    },
    {
        "category": "💭 Conhecimento Geral",
        "query": "Quem foi Albert Einstein?",
        "expected_tool": None
    },
    {
        "category": "💭 Conhecimento Geral",
        "query": "Explique o que é machine learning",
        "expected_tool": None
    },
]


def display_header() -> None:
    """Exibe o cabeçalho do script de demonstração."""
    header_text = Text()
    header_text.append("🎯 Demonstração do Assistente de IA\n\n", style="bold cyan")
    header_text.append("Este script executa ", style="")
    header_text.append(f"{len(DEMO_QUERIES)}", style="bold yellow")
    header_text.append(" consultas de exemplo para demonstrar\n", style="")
    header_text.append("as capacidades do assistente e suas ferramentas.\n\n", style="")
    header_text.append("Categorias:\n", style="bold yellow")
    header_text.append("  🧮 Calculadora - Cálculos matemáticos\n", style="")
    header_text.append("  📊 Estatística - Análise de dados\n", style="")
    header_text.append("  📅 Datas - Operações com datas\n", style="")
    header_text.append("  💭 Conhecimento Geral - Perguntas diretas\n", style="")

    panel = Panel(
        header_text,
        title="[bold magenta]Modo Demonstração[/bold magenta]",
        border_style="bright_blue",
        padding=(1, 2),
    )

    console.print(panel)
    console.print()


def display_query(index: int, total: int, category: str, query: str) -> None:
    """
    Exibe a consulta que será executada.

    Args:
        index: Índice da consulta (começando em 1)
        total: Total de consultas
        category: Categoria da consulta
        query: Texto da consulta
    """
    query_text = Text()
    query_text.append(f"[{index}/{total}] ", style="bold magenta")
    query_text.append(category, style="bold cyan")
    query_text.append(f"\n\n{query}", style="yellow")

    panel = Panel(
        query_text,
        title="[bold blue]📝 Pergunta[/bold blue]",
        border_style="blue",
        padding=(1, 2),
    )

    console.print(panel)


def display_result(response: str, tools_used: List[str], execution_time: float) -> None:
    """
    Exibe o resultado da consulta.

    Args:
        response: Resposta do assistente
        tools_used: Lista de ferramentas utilizadas
        execution_time: Tempo de execução em segundos
    """
    # Exibe a resposta
    console.print(Panel(
        Text(response, style="white"),
        title="[bold green]✅ Resposta[/bold green]",
        border_style="green",
        padding=(1, 2),
    ))

    # Exibe informações adicionais
    info_text = Text()

    if tools_used:
        info_text.append("🔧 Ferramenta: ", style="bold cyan")
        info_text.append(", ".join(tools_used), style="yellow")
    else:
        info_text.append("💭 Sem ferramentas (conhecimento direto)", style="dim italic")

    info_text.append(" | ", style="dim")
    info_text.append("⏱️  ", style="")
    info_text.append(f"{execution_time:.2f}s", style="bold magenta")

    console.print(info_text)
    console.print()


def main() -> None:
    """
    Função principal que executa todas as consultas de demonstração.
    """
    try:
        # Exibe cabeçalho
        display_header()

        # Estatísticas
        total_queries = len(DEMO_QUERIES)
        successful = 0
        failed = 0
        total_time = 0.0
        tools_usage = {}

        # Executa cada consulta
        for i, demo in enumerate(DEMO_QUERIES, 1):
            try:
                # Exibe a consulta
                display_query(i, total_queries, demo["category"], demo["query"])

                # Aguarda um momento para melhor visualização
                time.sleep(0.5)

                # Marca o tempo de início
                start_time = time.time()

                # Executa a consulta
                with console.status(
                    "[bold green]Processando...[/bold green]",
                    spinner="dots"
                ):
                    result = run_agent(demo["query"], verbose=False)

                # Calcula o tempo de execução
                execution_time = time.time() - start_time
                total_time += execution_time

                # Extrai resultados
                response = result.get("output", "Sem resposta")

                tools_used = []
                if "intermediate_steps" in result:
                    for step in result["intermediate_steps"]:
                        if len(step) > 0 and hasattr(step[0], 'tool'):
                            tool_name = step[0].tool
                            if tool_name not in tools_used:
                                tools_used.append(tool_name)
                                # Conta uso de ferramentas
                                tools_usage[tool_name] = tools_usage.get(tool_name, 0) + 1

                # Exibe o resultado
                display_result(response, tools_used, execution_time)

                successful += 1

                # Adiciona separador entre consultas (exceto na última)
                if i < total_queries:
                    console.print("─" * console.width, style="dim")
                    console.print()
                    # Pequena pausa entre consultas
                    time.sleep(1)

            except Exception as e:
                failed += 1
                console.print(
                    Panel(
                        f"[bold red]❌ Erro:[/bold red] {str(e)}",
                        border_style="red"
                    )
                )
                console.print()

        # Exibe resumo final
        console.print("\n")
        summary_text = Text()
        summary_text.append("📊 Resumo da Demonstração\n\n", style="bold cyan")

        summary_text.append("Resultados:\n", style="bold yellow")
        summary_text.append(f"  ✅ Sucessos: ", style="")
        summary_text.append(f"{successful}/{total_queries}\n", style="bold green")

        if failed > 0:
            summary_text.append(f"  ❌ Falhas: ", style="")
            summary_text.append(f"{failed}/{total_queries}\n", style="bold red")

        summary_text.append(f"\n⏱️  Tempo total: ", style="")
        summary_text.append(f"{total_time:.2f}s\n", style="bold magenta")
        summary_text.append(f"  Tempo médio: ", style="")
        summary_text.append(f"{total_time/total_queries:.2f}s\n", style="bold magenta")

        if tools_usage:
            summary_text.append(f"\n🔧 Uso de Ferramentas:\n", style="bold yellow")
            for tool, count in sorted(tools_usage.items()):
                summary_text.append(f"  • {tool}: ", style="")
                summary_text.append(f"{count}x\n", style="bold cyan")

        console.print(Panel(
            summary_text,
            title="[bold magenta]Demonstração Concluída[/bold magenta]",
            border_style="bright_blue",
            padding=(1, 2),
        ))

    except KeyboardInterrupt:
        console.print("\n")
        console.print(
            Panel(
                "[bold yellow]⚠️  Demonstração interrompida pelo usuário[/bold yellow]",
                border_style="yellow"
            )
        )

    except Exception as e:
        console.print()
        console.print(
            Panel(
                f"[bold red]❌ Erro fatal:[/bold red]\n{str(e)}",
                border_style="red",
                title="[bold red]Erro[/bold red]"
            )
        )
        raise


if __name__ == "__main__":
    main()
