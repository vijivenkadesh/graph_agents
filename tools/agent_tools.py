from langchain_core.tools import tool



@tool
def word_count_tool(text: str) -> int:
    """
    A tool that counts the number of words in a given text.
    """
    return len(text.split())
