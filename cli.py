import asyncio
import typer
from fastmcp import Client
from core.llm import LLMService
from core.models import ChatRequest
from core.settings import settings

app = typer.Typer()

MCP_URL = settings.mcp_url


async def pick_model() -> str:
    service = LLMService()
    models_page = await service.client.models.list()
    models = [m.id for m in models_page.data]

    typer.echo("\nAvailable models:")
    for i, model in enumerate(models, 1):
        typer.echo(f"  {i}. {model}")

    while True:
        raw = typer.prompt("\nPick a model (number)")
        if raw.isdigit() and 1 <= int(raw) <= len(models):
            return models[int(raw) - 1]
        typer.echo(f"Enter a number between 1 and {len(models)}")


async def pick_tool() -> str:
    async with Client(MCP_URL) as mcp:
        tools = await mcp.list_tools()

    typer.echo("\nAvailable tools:")
    for i, tool in enumerate(tools, 1):
        typer.echo(f"  {i}. {tool.name} — {tool.description}")

    while True:
        raw = typer.prompt("\nPick a tool (number)")
        if raw.isdigit() and 1 <= int(raw) <= len(tools):
            return f"{settings.mcp_server_label}-{tools[int(raw) - 1].name}"
        typer.echo(f"Enter a number between 1 and {len(tools)}")


async def chat_loop(tool_name: str, model: str) -> None:
    service = LLMService()
    typer.echo(
        f"\nUsing tool: {tool_name}  |  Model: {model}  |  Type 'quit' to exit.\n"
    )

    while True:
        message = typer.prompt("You")
        if message.strip().lower() == "quit":
            break

        request = ChatRequest(message=message, model=model, allowed_tools=[tool_name])
        response = await service.chat(request)
        typer.echo(f"\nAssistant: {response.text}\n")


async def run() -> None:
    model = await pick_model()
    tool_name = await pick_tool()
    await chat_loop(tool_name, model)


@app.command()
def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    app()
