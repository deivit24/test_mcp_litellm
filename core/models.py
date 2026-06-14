from pydantic import BaseModel


class MCPTool(BaseModel):
    type: str = "mcp"
    server_label: str
    server_url: str = "litellm_proxy"
    require_approval: str = "never"
    allowed_tools: list[str] | None = None


class ChatRequest(BaseModel):
    message: str
    model: str = "claude-haiku-4-5-20251001"
    allowed_tools: list[str] | None = None


class ChatResponse(BaseModel):
    text: str
    tool_used: str | None = None
