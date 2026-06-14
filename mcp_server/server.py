import httpx
import random
from fastmcp import FastMCP
from core.settings import settings

client = httpx.AsyncClient(base_url=settings.base_url)

openapi_spec = httpx.get(settings.base_url_docs).json()

mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="MCP Server Test API",
)


@mcp.tool
def roll_dice(n_dice: int) -> list[int]:
    """Roll `n_dice` 6-sided dice and return the results."""
    return [random.randint(1, 6) for _ in range(n_dice)]


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8001)
