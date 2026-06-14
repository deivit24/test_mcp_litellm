from openai import AsyncOpenAI
from core.models import ChatRequest, ChatResponse, MCPTool
from core.settings import settings


class LLMService:
    _MCP_SERVER_LABEL = "faq"

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key=settings.openai_key,
            base_url=settings.litellm_url,
        )

    async def chat(self, request: ChatRequest) -> ChatResponse:
        tool = MCPTool(
            server_label=self._MCP_SERVER_LABEL,
            allowed_tools=request.allowed_tools,
        )

        text_chunks: list[str] = []
        tool_used: str | None = None

        response = await self._client.responses.create(
            model=request.model,
            input=[{"role": "user", "content": request.message, "type": "message"}],
            tools=[tool.model_dump(exclude_none=True)],
            tool_choice="required" if request.allowed_tools else "auto",
            stream=True,
        )

        async for event in response:
            if event.type == "response.output_text.delta":
                text_chunks.append(event.delta)
            elif event.type == "response.output_item.done":
                if hasattr(event.item, "name") and event.item.type == "mcp_call":
                    tool_used = event.item.name

        return ChatResponse(text="".join(text_chunks), tool_used=tool_used)
