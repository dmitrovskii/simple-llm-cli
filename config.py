from pathlib import Path
import sys

from pydantic import ValidationError, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV = Path(__file__).resolve().parent / '.env'

class Settings(BaseSettings):

    service_api_key: SecretStr

    llm_model: str
    base_url: str

    model_config = SettingsConfigDict(
        env_file=ENV,
        env_file_encoding='utf-8'
    )

try:
    config = Settings() # type: ignore
except ValidationError as e:
    print("\n[ENV ERROR] Check the .env file. Missing required environment variables:")

    for error in e.errors(): 
        field_name = str(error["loc"][0])
        print(f"    - {field_name.upper()}")

    print("\nClose...")
    sys.exit(1)
