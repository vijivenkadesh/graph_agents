from fastmcp.tools import tool


@tool()
def word_count_tool(text: str) -> int:
    """
    A tool that counts the number of words in a given text.
    """
    return len(text.split())



@tool()
def profanity_check_tool(message: str) -> dict:
    """
        Check whether the given text contains common profanity words.

        Args:
            text (str): The input text to check for profanity.

        Returns:
            dict: A dictionary containing:
                - contains_profanity (bool): True if any profanity is found,
                otherwise False.
                - matched_words (list[str]): List of profanity words found
                in the input text.
                
    """

    profanity_words = {
        "idiot",
        "stupid",
        "damn",
        "shit",
        "fuck",
    }

    words = set(message.lower().split())

    found_words = words.intersection(profanity_words)

    return {
        "contains_profanity": bool(found_words),
        "matched_words": list(found_words),
    }



# if __name__ == "__main__":
#     message = "You are an Idiot"
#     result = profanity_check_tool(message=message)
#     print(result)