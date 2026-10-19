from config import config
from engine import ChatSession


def main() -> None:
    chat = ChatSession(
        api_key=config.service_api_key.get_secret_value(),
        base_url=config.base_url,
        model=config.llm_model
    )
    chat.chat()
    

if __name__ == '__main__':
    main()

