def main():
    print("Hello from graph-agents!")
    from core.config import EnvSettings

    settings = EnvSettings()
    print(settings.OPENAI_API_KEY)
    print(settings.MODEL)


if __name__ == "__main__":
    main()
