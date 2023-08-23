
from langchain.tools import BaseTool
class CustomBrowser(BaseTool):
    name = "Zscaler Browser"
    description = "useful for when you need to answer questions about zscaler company"

    def _run(
        self, query: str) -> str:
        """Use the tool."""
        return " No answer"

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Calculator does not support async")