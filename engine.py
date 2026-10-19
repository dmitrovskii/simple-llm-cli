import json
from collections import deque
from pathlib import Path

from openai import OpenAI

class ChatSession:

    DEFAULT_INSTRUCTION = (
        "System Instructions:\n"
        "1. Output plain text only. Do not use Markdown, HTML, or any formatting syntax (no bold, lists, headers, etc.).\n"
        "2. Respond in the exact language used by the user."
    )

    def __init__(
            self, 
            api_key: str, 
            base_url: str,
            model: str, 
            chat_length: int = 20
            ) -> None:
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

        self.content_path = Path(__file__).resolve().parent / "content"
        self.history_file = self.content_path / "history.json"
        self.instruction_file = self.content_path / "instruction.txt"

        self.llm_model = model
        self.maxlen = chat_length
        self.history = self._history_load()
        self.instruct = self._instruct_load()


    def _instruct_load(self) -> str:
        if not self.instruction_file.exists():
            self.instruction_file.parent.mkdir(parents=True, exist_ok=True)
            self.instruction_file.write_text(self.DEFAULT_INSTRUCTION, encoding="utf-8")
            return self.DEFAULT_INSTRUCTION
        
        return self.instruction_file.read_text(encoding="utf-8")


    def _history_load(self) -> deque[dict]: 
        if not self.history_file.exists():
            return deque(maxlen=self.maxlen)

        try:
            data = json.loads(self.history_file.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return deque(data, maxlen=self.maxlen)
            return deque(maxlen=self.maxlen)
        
        except (json.JSONDecodeError, OSError) as e:
            print(f"Context error is: {e}")
            return deque(maxlen=self.maxlen)

        
    def save_history(self) -> None:
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.history_file.write_text(
            json.dumps(list(self.history), indent=4, ensure_ascii=False),
            encoding="utf-8"
        )


    def process_text(self, text: str) -> str | None:
        user_request = {"role": "user", "content": text}

        response = self.client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": self.instruct}, 
                *self.history, 
                user_request
                ],
            temperature=0.5
        )

        assistant_content = response.choices[0].message.content

        self.history.extend([
            user_request,
            {"role": "assistant", "content": assistant_content}
        ])

        return assistant_content
    

    def chat(self) -> None:
        print('Write "exit" for exit.\n')

        try: 
            while True:
                try: 
                    user = input("User:\n").strip()
                except EOFError: 
                    print("\nExit...")
                    break

                if user.lower() == "exit":
                    break

                if not user: 
                    continue

                try: 
                    answer = self.process_text(text=user)
                    print(f"\nModel:\n{answer}\n")

                except Exception as e: 
                    print(f"\r\033[31m[Error API]: {e}\033[0m\n")

        except KeyboardInterrupt:
            print("\nExit...")

        finally: 
            self.save_history()