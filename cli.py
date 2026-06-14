import asyncio
import typer
from fastmcp import Client
from core.llm import LLMService
from core.models import ChatRequest
from core.settings import settings

app = typer.Typer()

MCP_URL = settings.mcp_url


async def pick_tool() -> str:
    async with Client(MCP_URL) as mcp:
        tools = await mcp.list_tools()

    typer.echo("\nAvailable tools:")
    for i, tool in enumerate(tools, 1):
        typer.echo(f"  {i}. {tool.name} — {tool.description}")

    while True:
        raw = typer.prompt("\nPick a tool (number)")
        if raw.isdigit() and 1 <= int(raw) <= len(tools):
            return tools[int(raw) - 1].name
        typer.echo(f"Enter a number between 1 and {len(tools)}")


async def chat_loop(tool_name: str) -> None:
    service = LLMService()
    typer.echo(f"\nUsing tool: {tool_name}  |  Type 'quit' to exit.\n")

    while True:
        message = typer.prompt("You")
        if message.strip().lower() == "quit":
            break

        request = ChatRequest(message=message, allowed_tools=[tool_name])
        response = await service.chat(request)
        typer.echo(f"\nAssistant: {response.text}\n")


async def run() -> None:
    tool_name = await pick_tool()
    await chat_loop(tool_name)


@app.command()
def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    app()
