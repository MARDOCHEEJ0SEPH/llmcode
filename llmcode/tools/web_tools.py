"""Web-related tools"""

import requests
from typing import Any, Dict, Optional
from .base import Tool, ToolResult, ToolStatus


class WebSearchTool(Tool):
    """Tool for web search (requires API key)"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    @property
    def name(self) -> str:
        return "WebSearch"

    @property
    def description(self) -> str:
        return "Searches the web and returns results. Requires SERPER_API_KEY."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                }
            },
            "required": ["query"]
        }

    def execute(self, query: str) -> ToolResult:
        """Perform web search"""
        if not self.api_key:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error="Web search requires SERPER_API_KEY to be configured"
            )

        try:
            response = requests.post(
                "https://google.serper.dev/search",
                headers={
                    "X-API-KEY": self.api_key,
                    "Content-Type": "application/json"
                },
                json={"q": query},
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            results = []

            # Parse organic results
            for item in data.get("organic", [])[:5]:
                results.append(f"Title: {item.get('title')}")
                results.append(f"URL: {item.get('link')}")
                results.append(f"Snippet: {item.get('snippet')}")
                results.append("")

            output = "\n".join(results) if results else "No results found"

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={"query": query, "result_count": len(data.get("organic", []))}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Web search error: {str(e)}"
            )


class WebFetchTool(Tool):
    """Tool for fetching web page content"""

    @property
    def name(self) -> str:
        return "WebFetch"

    @property
    def description(self) -> str:
        return "Fetches content from a URL and returns the text"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to fetch"
                }
            },
            "required": ["url"]
        }

    def execute(self, url: str) -> ToolResult:
        """Fetch web page content"""
        try:
            response = requests.get(
                url,
                headers={"User-Agent": "LLMCode/0.1.0"},
                timeout=10
            )
            response.raise_for_status()

            # Simple text extraction (could be enhanced with BeautifulSoup)
            content = response.text[:10000]  # Limit content size

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=content,
                metadata={
                    "url": url,
                    "status_code": response.status_code,
                    "content_type": response.headers.get("content-type")
                }
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error fetching URL: {str(e)}"
            )
