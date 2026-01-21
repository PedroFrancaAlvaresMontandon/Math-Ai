"""
Interactive CLI application for the AI Assistant with LangChain.

This is the main entry point to interact with the AI assistant
that has access to specialized tools for mathematical calculations,
statistical analysis, and date operations.
"""
import time
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.rule import Rule
from rich import print as rprint

from src.agent.agent import run_agent
from src.utils.logger import logger


console = Console()


def display_welcome_banner() -> None:
    """
    Displays the welcome banner with information about the assistant.
    """
    welcome_text = Text()
    welcome_text.append("🤖 Assistente de IA com Ferramentas LangChain\n\n", style="bold cyan")
    welcome_text.append("Ferramentas disponíveis:\n", style="bold yellow")
    welcome_text.append("  🧮 ", style="")
    welcome_text.append("Calculator", style="bold green")
    welcome_text.append(" - Cálculos matemáticos e expressões\n", style="")
    welcome_text.append("  📊 ", style="")
    welcome_text.append("Statistics Analyzer", style="bold green")
    welcome_text.append(" - Análise estatística de dados\n", style="")
    welcome_text.append("  📅 ", style="")
    welcome_text.append("Date Calculator", style="bold green")
    welcome_text.append(" - Operações com datas\n\n", style="")
    welcome_text.append("💡 Dicas:\n", style="bold yellow")
    welcome_text.append("  • Faça perguntas em linguagem natural\n", style="dim")
    welcome_text.append("  • O assistente escolherá a ferramenta apropriada\n", style="dim")
    welcome_text.append("  • Digite ", style="dim")
    welcome_text.append("'exit'", style="bold red")
    welcome_text.append(" ou ", style="dim")
    welcome_text.append("'quit'", style="bold red")
    welcome_text.append(" para sair\n", style="dim")
    welcome_text.append("  • Use ", style="dim")
    welcome_text.append("Ctrl+C", style="bold red")
    welcome_text.append(" para interromper\n", style="dim")

    panel = Panel(
        welcome_text,
        title="[bold magenta]Bem-vindo![/bold magenta]",
        border_style="bright_blue",
        padding=(1, 2),
    )

    console.print(panel)
    console.print()


def display_response(
    query: str,
    response: str,
    tools_used: list,
    execution_time: float
) -> None:
    """
    Displays the assistant's response in formatted form.

    Args:
        query: User question
        response: Assistant response
        tools_used: List of tools used
        execution_time: Execution time in seconds
    """
    # Display the response
    response_panel = Panel(
        Text(response, style="white"),
        title="[bold green]🤖 Assistente[/bold green]",
        border_style="green",
        padding=(1, 2),
    )
    console.print(response_panel)

    # Display additional information
    info_text = Text()

    if tools_used:
        info_text.append("🔧 Ferramentas usadas: ", style="bold cyan")
        info_text.append(", ".join(tools_used), style="yellow")
        info_text.append(" | ", style="dim")
    else:
        info_text.append("💭 Resposta direta (sem ferramentas)", style="dim italic")
        info_text.append(" | ", style="dim")

    info_text.append("⏱️  ", style="")
    info_text.append(f"{execution_time:.2f}s", style="bold magenta")

    console.print(info_text)
    console.print()


def main() -> None:
    """
    Main function that runs the assistant's interactive loop.
    """
    try:
        # Display welcome banner
        display_welcome_banner()

        query_count = 0

        # Main interaction loop
        while True:
            try:
                # Request user input
                user_input = Prompt.ask(
                    "[bold blue]Você[/bold blue]",
                    default=""
                )

                # Remove whitespace
                user_input = user_input.strip()

                # Check exit commands
                if user_input.lower() in ['exit', 'quit', 'sair', 'q']:
                    console.print()
                    console.print(
                        Panel(
                            "[bold yellow]👋 Até logo! Foi um prazer ajudar você.[/bold yellow]",
                            border_style="yellow"
                        )
                    )
                    break

                # Ignore empty inputs
                if not user_input:
                    continue

                query_count += 1

                # Mark start time
                start_time = time.time()

                # Process the query
                console.print()
                with console.status(
                    "[bold green]Processando sua pergunta...[/bold green]",
                    spinner="dots"
                ):
                    result = run_agent(user_input)

                # Calculate execution time
                execution_time = time.time() - start_time

                # Extract response and tools used
                response = result.get("output", "Desculpe, não consegui gerar uma resposta.")

                tools_used = []
                if "intermediate_steps" in result:
                    for step in result["intermediate_steps"]:
                        if len(step) > 0 and hasattr(step[0], 'tool'):
                            tool_name = step[0].tool
                            if tool_name not in tools_used:
                                tools_used.append(tool_name)

                # Display the response
                display_response(user_input, response, tools_used, execution_time)

                # Add visual separator
                console.print(Rule(style="dim"))
                console.print()

            except KeyboardInterrupt:
                console.print("\n")
                console.print(
                    Panel(
                        "[bold yellow]👋 Interrompido pelo usuário. Até logo![/bold yellow]",
                        border_style="yellow"
                    )
                )
                break

            except Exception as e:
                console.print()
                console.print(
                    Panel(
                        f"[bold red]❌ Erro ao processar consulta:[/bold red]\n{str(e)}",
                        border_style="red",
                        title="[bold red]Erro[/bold red]"
                    )
                )
                console.print()
                logger.error(f"Erro na consulta: {str(e)}")

        # Display final statistics
        if query_count > 0:
            console.print()
            stats_text = Text()
            stats_text.append("📊 Estatísticas da sessão:\n", style="bold cyan")
            stats_text.append(f"  • Total de consultas: ", style="")
            stats_text.append(f"{query_count}", style="bold yellow")

            console.print(Panel(stats_text, border_style="cyan"))

    except Exception as e:
        console.print()
        console.print(
            Panel(
                f"[bold red]❌ Erro crítico:[/bold red]\n{str(e)}",
                border_style="red",
                title="[bold red]Erro Fatal[/bold red]"
            )
        )
        logger.error(f"Erro crítico: {str(e)}")
        raise


if __name__ == "__main__":
    main()
