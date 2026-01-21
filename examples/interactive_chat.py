"""
Chat interativo avançado com histórico e estatísticas.

Este script fornece uma experiência de chat aprimorada com:
- Histórico de conversação
- Estatísticas detalhadas de uso
- Opção de salvar conversas
- Interface visual rica
"""
import time
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.table import Table
from rich.rule import Rule
from rich import print as rprint

from src.agent.agent import run_agent
from src.utils.logger import logger


console = Console()


class ChatSession:
    """Gerencia uma sessão de chat com histórico e estatísticas."""

    def __init__(self):
        """Inicializa uma nova sessão de chat."""
        self.messages: List[Dict[str, str]] = []
        self.start_time = datetime.now()
        self.total_execution_time = 0.0
        self.query_count = 0
        self.tools_usage: Dict[str, int] = {}

    def add_message(self, role: str, content: str, tools_used: Optional[List[str]] = None) -> None:
        """
        Adiciona uma mensagem ao histórico.

        Args:
            role: 'user' ou 'assistant'
            content: Conteúdo da mensagem
            tools_used: Lista de ferramentas utilizadas (opcional)
        """
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "tools": tools_used or []
        })

        # Atualiza estatísticas de ferramentas
        if tools_used:
            for tool in tools_used:
                self.tools_usage[tool] = self.tools_usage.get(tool, 0) + 1

    def get_statistics(self) -> Dict:
        """
        Retorna estatísticas da sessão.

        Returns:
            Dicionário com estatísticas
        """
        duration = datetime.now() - self.start_time
        return {
            "query_count": self.query_count,
            "total_time": self.total_execution_time,
            "avg_time": self.total_execution_time / self.query_count if self.query_count > 0 else 0,
            "session_duration": duration.total_seconds(),
            "tools_usage": self.tools_usage,
            "message_count": len(self.messages)
        }

    def save_to_file(self, filepath: str) -> None:
        """
        Salva o histórico de conversação em um arquivo.

        Args:
            filepath: Caminho do arquivo para salvar
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"HISTÓRICO DE CONVERSAÇÃO - {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")

            for msg in self.messages:
                role_display = "👤 VOCÊ" if msg["role"] == "user" else "🤖 ASSISTENTE"
                timestamp = datetime.fromisoformat(msg["timestamp"]).strftime('%H:%M:%S')

                f.write(f"\n[{timestamp}] {role_display}\n")
                f.write("-" * 80 + "\n")
                f.write(f"{msg['content']}\n")

                if msg.get("tools"):
                    f.write(f"\n🔧 Ferramentas: {', '.join(msg['tools'])}\n")

            # Adiciona estatísticas
            stats = self.get_statistics()
            f.write("\n\n" + "=" * 80 + "\n")
            f.write("ESTATÍSTICAS DA SESSÃO\n")
            f.write("=" * 80 + "\n")
            f.write(f"Total de consultas: {stats['query_count']}\n")
            f.write(f"Tempo total de execução: {stats['total_time']:.2f}s\n")
            f.write(f"Tempo médio por consulta: {stats['avg_time']:.2f}s\n")
            f.write(f"Duração da sessão: {stats['session_duration']:.0f}s\n")

            if stats['tools_usage']:
                f.write(f"\nUso de ferramentas:\n")
                for tool, count in sorted(stats['tools_usage'].items()):
                    f.write(f"  • {tool}: {count}x\n")


def display_welcome_banner() -> None:
    """Exibe o banner de boas-vindas."""
    welcome_text = Text()
    welcome_text.append("💬 Chat Interativo Avançado\n\n", style="bold cyan")
    welcome_text.append("Recursos especiais:\n", style="bold yellow")
    welcome_text.append("  📝 Histórico de conversação completo\n", style="")
    welcome_text.append("  📊 Estatísticas detalhadas de uso\n", style="")
    welcome_text.append("  💾 Opção de salvar conversas\n", style="")
    welcome_text.append("  🎨 Interface visual aprimorada\n\n", style="")

    welcome_text.append("Ferramentas disponíveis:\n", style="bold yellow")
    welcome_text.append("  🧮 Calculator - Cálculos matemáticos\n", style="")
    welcome_text.append("  📊 Statistics - Análise estatística\n", style="")
    welcome_text.append("  📅 Date Calculator - Operações com datas\n\n", style="")

    welcome_text.append("Comandos especiais:\n", style="bold yellow")
    welcome_text.append("  • ", style="")
    welcome_text.append("stats", style="bold cyan")
    welcome_text.append(" - Ver estatísticas da sessão\n", style="")
    welcome_text.append("  • ", style="")
    welcome_text.append("history", style="bold cyan")
    welcome_text.append(" - Ver histórico de mensagens\n", style="")
    welcome_text.append("  • ", style="")
    welcome_text.append("clear", style="bold cyan")
    welcome_text.append(" - Limpar a tela\n", style="")
    welcome_text.append("  • ", style="")
    welcome_text.append("exit/quit", style="bold red")
    welcome_text.append(" - Sair do chat\n", style="")

    panel = Panel(
        welcome_text,
        title="[bold magenta]Bem-vindo![/bold magenta]",
        border_style="bright_blue",
        padding=(1, 2),
    )

    console.print(panel)
    console.print()


def display_statistics(session: ChatSession) -> None:
    """
    Exibe estatísticas da sessão.

    Args:
        session: Sessão de chat atual
    """
    stats = session.get_statistics()

    # Cria tabela de estatísticas gerais
    table = Table(title="📊 Estatísticas da Sessão", border_style="cyan")
    table.add_column("Métrica", style="bold yellow")
    table.add_column("Valor", style="bold green")

    table.add_row("Total de consultas", str(stats['query_count']))
    table.add_row("Mensagens totais", str(stats['message_count']))
    table.add_row("Tempo total de execução", f"{stats['total_time']:.2f}s")

    if stats['query_count'] > 0:
        table.add_row("Tempo médio por consulta", f"{stats['avg_time']:.2f}s")

    table.add_row("Duração da sessão", f"{stats['session_duration']:.0f}s")

    console.print(table)

    # Exibe uso de ferramentas se houver
    if stats['tools_usage']:
        console.print()
        tools_table = Table(title="🔧 Uso de Ferramentas", border_style="cyan")
        tools_table.add_column("Ferramenta", style="bold yellow")
        tools_table.add_column("Vezes usada", style="bold green")

        for tool, count in sorted(stats['tools_usage'].items(), key=lambda x: x[1], reverse=True):
            tools_table.add_row(tool, str(count))

        console.print(tools_table)

    console.print()


def display_history(session: ChatSession, limit: int = 10) -> None:
    """
    Exibe o histórico de mensagens.

    Args:
        session: Sessão de chat atual
        limit: Número máximo de mensagens a exibir
    """
    if not session.messages:
        console.print(Panel(
            "[yellow]Nenhuma mensagem no histórico ainda.[/yellow]",
            border_style="yellow"
        ))
        return

    messages_to_show = session.messages[-limit:] if len(session.messages) > limit else session.messages

    console.print(Panel(
        f"[bold cyan]Exibindo últimas {len(messages_to_show)} mensagens[/bold cyan]",
        border_style="cyan"
    ))
    console.print()

    for msg in messages_to_show:
        role_icon = "👤" if msg["role"] == "user" else "🤖"
        role_name = "Você" if msg["role"] == "user" else "Assistente"
        role_style = "blue" if msg["role"] == "user" else "green"

        timestamp = datetime.fromisoformat(msg["timestamp"]).strftime('%H:%M:%S')

        console.print(f"[{role_style}]{role_icon} {role_name}[/{role_style}] [dim]({timestamp})[/dim]")
        console.print(f"  {msg['content']}")

        if msg.get("tools"):
            console.print(f"  [dim]🔧 Ferramentas: {', '.join(msg['tools'])}[/dim]")

        console.print()


def main() -> None:
    """Função principal do chat interativo."""
    try:
        # Inicializa a sessão
        session = ChatSession()

        # Exibe banner de boas-vindas
        display_welcome_banner()

        # Loop principal
        while True:
            try:
                # Solicita entrada do usuário
                user_input = Prompt.ask(
                    "[bold blue]Você[/bold blue]",
                    default=""
                )

                user_input = user_input.strip()

                # Comandos especiais
                if user_input.lower() in ['exit', 'quit', 'sair', 'q']:
                    # Pergunta se quer salvar o histórico
                    if session.messages:
                        console.print()
                        save = Confirm.ask(
                            "[yellow]Deseja salvar o histórico da conversação?[/yellow]"
                        )

                        if save:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"chat_history_{timestamp}.txt"
                            filepath = Path("conversas") / filename

                            # Cria diretório se não existir
                            filepath.parent.mkdir(exist_ok=True)

                            session.save_to_file(str(filepath))

                            console.print(
                                Panel(
                                    f"[bold green]✅ Histórico salvo em:[/bold green]\n{filepath}",
                                    border_style="green"
                                )
                            )

                    console.print()
                    console.print(
                        Panel(
                            "[bold yellow]👋 Até logo! Foi um prazer conversar com você.[/bold yellow]",
                            border_style="yellow"
                        )
                    )

                    # Exibe estatísticas finais
                    if session.query_count > 0:
                        console.print()
                        display_statistics(session)

                    break

                elif user_input.lower() == 'stats':
                    console.print()
                    display_statistics(session)
                    continue

                elif user_input.lower() == 'history':
                    console.print()
                    display_history(session)
                    continue

                elif user_input.lower() == 'clear':
                    console.clear()
                    display_welcome_banner()
                    continue

                # Ignora entradas vazias
                if not user_input:
                    continue

                # Adiciona mensagem do usuário ao histórico
                session.add_message("user", user_input)
                session.query_count += 1

                # Processa a consulta
                console.print()
                start_time = time.time()

                with console.status(
                    "[bold green]Processando...[/bold green]",
                    spinner="dots"
                ):
                    result = run_agent(user_input, verbose=False)

                execution_time = time.time() - start_time
                session.total_execution_time += execution_time

                # Extrai resultados
                response = result.get("output", "Desculpe, não consegui gerar uma resposta.")

                tools_used = []
                if "intermediate_steps" in result:
                    for step in result["intermediate_steps"]:
                        if len(step) > 0 and hasattr(step[0], 'tool'):
                            tool_name = step[0].tool
                            if tool_name not in tools_used:
                                tools_used.append(tool_name)

                # Adiciona resposta ao histórico
                session.add_message("assistant", response, tools_used)

                # Exibe a resposta
                response_panel = Panel(
                    Text(response, style="white"),
                    title="[bold green]🤖 Assistente[/bold green]",
                    border_style="green",
                    padding=(1, 2),
                )
                console.print(response_panel)

                # Exibe informações
                info_text = Text()
                if tools_used:
                    info_text.append("🔧 Ferramentas: ", style="bold cyan")
                    info_text.append(", ".join(tools_used), style="yellow")
                else:
                    info_text.append("💭 Resposta direta", style="dim italic")

                info_text.append(" | ", style="dim")
                info_text.append("⏱️  ", style="")
                info_text.append(f"{execution_time:.2f}s", style="bold magenta")
                info_text.append(" | ", style="dim")
                info_text.append(f"Consulta #{session.query_count}", style="dim")

                console.print(info_text)
                console.print()
                console.print(Rule(style="dim"))
                console.print()

            except KeyboardInterrupt:
                console.print("\n")
                console.print(
                    Panel(
                        "[bold yellow]⚠️  Use 'exit' para sair com opção de salvar histórico[/bold yellow]",
                        border_style="yellow"
                    )
                )
                console.print()
                continue

            except Exception as e:
                console.print()
                console.print(
                    Panel(
                        f"[bold red]❌ Erro:[/bold red]\n{str(e)}",
                        border_style="red"
                    )
                )
                console.print()
                logger.error(f"Erro: {str(e)}")

    except Exception as e:
        console.print()
        console.print(
            Panel(
                f"[bold red]❌ Erro fatal:[/bold red]\n{str(e)}",
                border_style="red",
                title="[bold red]Erro[/bold red]"
            )
        )
        logger.error(f"Erro fatal: {str(e)}")
        raise


if __name__ == "__main__":
    main()
