"""
Agent Module - LangGraph with Tool Calling
"""

from typing import Dict, Any, Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage

from src.tools.calculator import calculator
from src.tools.statistics import statistics_analyzer
from src.tools.date_calculator import date_calculator
from src.llm.client import get_llm
from src.utils.logger import get_logger

logger = get_logger(__name__)
_agent_graph = None


class AgentState(TypedDict):
    """Agent state."""
    messages: Annotated[list, add_messages]


def create_agent_graph():
    """Creates the agent graph with tool calling."""

    # Available tools
    tools = [calculator, statistics_analyzer, date_calculator]
    tool_map = {tool.name: tool for tool in tools}

    # LLM with bound tools
    llm = get_llm()
    llm_with_tools = llm.bind_tools(tools)

    # System prompt that instructs WHEN to use tools
    system_prompt = """Você é um assistente de IA útil com acesso a ferramentas especializadas.

🔧 FERRAMENTAS DISPONÍVEIS:

1. **calculator** - Use para QUALQUER operação matemática:
   - Multiplicação, divisão, soma, subtração
   - Potências, raízes quadradas
   - Funções trigonométricas
   - Exemplos: "quanto é 128 * 46?", "raiz de 144", "2 elevado a 8"

2. **statistics_analyzer** - Use para análise estatística:
   - Média, mediana, moda
   - Desvio padrão, variância
   - Quartis
   - Exemplo: "calcule a média de 10, 20, 30, 40, 50"

3. **date_calculator** - Use para operações com datas:
   - Diferença entre datas
   - Adicionar/subtrair dias
   - Calcular idade
   - Dia da semana
   - Exemplo: "quantos anos tenho se nasci em 1990-03-15?"

⚠️ QUANDO USAR FERRAMENTAS:
- Se a pergunta envolve CÁLCULO → use calculator
- Se a pergunta envolve ANÁLISE de números → use statistics_analyzer
- Se a pergunta envolve DATAS → use date_calculator
- Se é conhecimento geral → responda diretamente SEM ferramenta

✅ Sempre responda em português brasileiro de forma natural e clara."""

    # Node that calls the LLM
    def call_model(state: AgentState):
        messages = state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    # Node that executes tools
    def call_tools(state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]

        tool_results = []
        for tool_call in last_message.tool_calls:
            tool = tool_map[tool_call["name"]]
            result = tool.invoke(tool_call["args"])

            tool_message = ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]
            )
            tool_results.append(tool_message)

        return {"messages": tool_results}

    # Decides whether to continue (has tool calls) or end
    def should_continue(state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]

        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        return "end"

    # Create the graph
    workflow = StateGraph(AgentState)

    workflow.add_node("agent", call_model)
    workflow.add_node("tools", call_tools)

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )

    workflow.add_edge("tools", "agent")

    # Compile with system message
    app = workflow.compile()

    # Wrapper that automatically adds system message
    def agent_with_system(inputs):
        messages = inputs.get("messages", [])
        # Add system message if it doesn't exist
        if not any(isinstance(m, SystemMessage) for m in messages):
            messages = [SystemMessage(content=system_prompt)] + messages
        return app.invoke({"messages": messages})

    return agent_with_system


def get_agent():
    """Gets or creates the agent."""
    global _agent_graph

    if _agent_graph is None:
        try:
            logger.info("Criando agente LangGraph com tool calling")
            _agent_graph = create_agent_graph()
            logger.info("Agente criado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao criar agente: {str(e)}")
            raise

    return _agent_graph


def run_agent(query: str) -> Dict[str, Any]:
    """Runs the agent with a query."""
    try:
        agent = get_agent()
        logger.info(f"Processando: {query[:50]}...")

        # Invoke the agent with user message
        result = agent({
            "messages": [HumanMessage(content=query)]
        })

        logger.info("Consulta processada com sucesso")

        # Extract final response and tools used
        messages = result.get("messages", [])
        output = ""
        tools_used = []

        for msg in messages:
            # Find the final response
            if isinstance(msg, AIMessage) and msg.content:
                output = msg.content

            # Detect which tools were called
            if isinstance(msg, AIMessage) and hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tool_name = tool_call.get('name', '')
                    if tool_name and tool_name not in tools_used:
                        tools_used.append(tool_name)

        # Format intermediate_steps for main.py
        intermediate_steps = []
        if tools_used:
            # Create a structure that main.py expects
            for tool_name in tools_used:
                # Simulate the format expected by main.py
                class ToolAction:
                    def __init__(self, tool):
                        self.tool = tool
                intermediate_steps.append((ToolAction(tool_name), ""))

        return {
            "output": output or "Desculpe, não consegui gerar uma resposta.",
            "intermediate_steps": intermediate_steps
        }

    except Exception as e:
        logger.error(f"Erro ao executar agente: {str(e)}")
        return {
            "output": f"Desculpe, ocorreu um erro: {str(e)}",
            "intermediate_steps": []
        }


def reset_agent():
    """Resets the global agent."""
    global _agent_graph
    _agent_graph = None
    logger.info("Agente resetado")
