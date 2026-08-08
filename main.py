from utils.llm_manager import LLMManager

def main():
    llm_manager = LLMManager()
    llm = llm_manager.load_model()
    response = llm.invoke(input="HI how are you")
    result = response.content
    print(result)


if __name__ == "__main__":
    main()
