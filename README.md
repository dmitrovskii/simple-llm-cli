# **Simple LLM CLI**

A lightweight, terminal-based chat client with persistent conversation memory. Built on top of the official OpenAI Python SDK, it works out of the box with any OpenAI-compatible provider (Google Gemini, OpenAI, Groq, OpenRouter) as well as self-hosted local models (Ollama, vLLM, LM Studio).

### Supported Providers & Compatibility

Configure your target provider in `.env` by supplying its base URL, API key, and model identifier:

| Provider | Base URL | Example Model |
| :--- | :--- | :--- |
| **Google Gemini** | `https://generativelanguage.googleapis.com/v1beta/openai/` | `gemini-3.5-flash-lite` | 
| **OpenAI** | `https://api.openai.com/v1/chat/completions` | `gpt-5.6-terra` | 
| **Groq** | `https://api.groq.com/openai/v1/chat/completions` | `openai/gpt-oss-120b` | 
| **OpenRouter** | `https://openrouter.ai/api/v1/chat/completions` | `meta-llama/llama-3.3-70b-instruct` | 
| **Ollama (Local)** | `http://localhost:11434/v1` | `llama3.2` | 

---

## Features
- **Sliding Window Memory:** Uses `collections.deque` to maintain recent conversational flow while preventing token bloat.
- **Atomic State Updates:** Context history updates only upon successful API responses, keeping sessions clean from network failures.
- **Session Persistence:** Automatically saves and restores conversation history (`history.json`) across application restarts.
- **Customizable Persona:** Automatically generates `instruction.txt` on first launch for custom system prompts and constraints.
- **Robust Configuration:** Powered by `pydantic-settings` for type-safe environment variable parsing and secure key handling.
- **Cross-Platform:** Works seamlessly across Linux, macOS, and Windows.

---

## Tech Stack
- **Python 3.14+**
- **OpenAI Python SDK**
- **Pydantic Settings**
- **Standard Library:** `collections.deque`, `pathlib.Path`, `json`

---

## Quick Start

### 1. Clone the repository
   ``` bash
   git clone https://github.com/dmitrovskii/simple-llm-cli.git
   cd simple-llm-cli
   ```
### 2. Create and activate a virtual environment

   ``` bash
   # Create virtual environment
   python -m venv .venv

   # Activate (Linux / macOS)
   source .venv/bin/activate

   # Activate (Windows)
   .venv\Scripts\activate
   ```
### 3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

### 4. Configure environment variables
   Copy the example environment file and specify your API tokens, model 
   ``` bash
   cp .env.example .env
   ```

   Open .env in any editor and set:

   ``` bash
   LLM_MODEL="gemini-3.5-flash-lite"
   SERVICE_API_KEY="your_api_key"
   BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
   ```

   > **Using Ollama?** Set BASE_URL="http://localhost:11434/v1" and pass any arbitrary string (e.g., ollama) as SERVICE_API_KEY

### 5. Launch
   ```
   python main.py
   ```
   Type exit or press Ctrl+C to quit and save the session.

---

## Project Structure
``` bash
simple-llm-cli/
├── content/               # Auto-generated runtime data (ignored by git)
│   ├── history.json       # Persisted sliding-window chat history
│   └── instruction.txt    # System instructions / assistant persona
├── config.py              # Pydantic Settings configuration loader
├── engine.py              # Core ChatSession manager & CLI loop
├── main.py                # Composition root & entry point
└── requirements.txt
```
---
## Author & License
* **Author:** @dmitrovskii
* **License:** MIT License