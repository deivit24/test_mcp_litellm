import httpx
import random
from fastmcp import FastMCP
from core.settings import settings

if not settings.base_url:
    raise ValueError("BASE_URL is not set")
if not settings.base_url_docs:
    raise ValueError("BASE_URL_DOCS is not set")

print(f"BASE_URL:      {settings.base_url}")
print(f"BASE_URL_DOCS: {settings.base_url_docs}")
print(f"MCP_URL:       {settings.mcp_url}")

client = httpx.AsyncClient(base_url=settings.base_url)

_response = httpx.get(settings.base_url_docs)
_response.raise_for_status()
openapi_spec = _response.json()

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
