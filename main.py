from google.genai import types

from engine import GoogleTerminalGets
from engine import ChatMemory
from config import config

def main():

    chat = None
    model = None

    try:
        model = GoogleTerminalGets(
            model_name=config.llm_model,
            api_key=config.service_api_key.get_secret_value()            
        )
        chat = ChatMemory()

        instructions = [
            types.Content(role="user", parts=[types.Part(text=f"SYSTEM INSTRUCTION: {model.instruct}")])
        ]
        
        history = chat.history

        while True:
            user_text = input("[User]: ")
            history.extend([
                types.Content(role="user", parts=[types.Part(text=user_text)])
            ])

            response = model.ask(
                [*instructions, *history]
            )  

            history.extend([
                types.Content(role="model", parts=[types.Part(text=response)])
            ])

            print(f"\n[Model]: {response}")

    except KeyboardInterrupt:
        print("\nClose...")
    except ValueError:
        print("\033[33mThe key.txt file is empty. Please insert into file your API-key.\033[0m")
    finally:
        if chat is not None:
            chat.save_history(chat.convert(history))

if __name__ == '__main__':
    main()

