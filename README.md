# Offline Multilingual Chatbot — Web

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/Offline--First-238636?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Active_Development-ff5e6c?style=for-the-badge" />
</p>

> **A modular Python chatbot with offline-first conversation, multilingual support, games, tools, memory, optional ML, and optional LLM fallback.**

This project grew from a lightweight Android/Pydroid chatbot into a modular Python system with a clear separation between conversational handlers, intent processing, memory, tools, and optional intelligence backends.

## Highlights

- English, Kiswahili, and French
- Rule-based intent engine with optional ML backends
- Conversation memory and tone tracking
- Creative writing: poems, stories, jokes, riddles and more
- Games and learning utilities
- Math, conversions, text tools, QR generation and other utilities
- Optional computer-vision features
- Offline voice input through Vosk
- Optional PyTorch/Keras/scikit-learn integrations
- Optional Claude/GPT fallback — never required for core operation
- Designed to retain an offline path for Android/Pydroid 3

## Architecture

```text
chatbot_modules/
    numbered source modules
          │
          ▼
      main.py
          │
          ▼
    shared runtime namespace
          │
          ├── Intent / NLP
          ├── Conversation handlers
          ├── Memory
          ├── Games
          ├── Tools
          └── Response banks

src/chatbot/
    installable package layer
          │
          └── clean Python imports
```

## Installation

Python 3.9+ is recommended.

Core CLI operation has no mandatory third-party dependency:

```bash
git clone <this-repository>
cd <this-repository>
python chatbot_modules/main.py --text
```

Optional feature groups:

| Feature | Install |
|---|---|
| Kivy GUI | `pip install .[gui]` |
| Vision | `pip install .[vision]` |
| Classical ML | `pip install .[ml]` |
| PyTorch | `pip install .[ml-torch]` |
| Offline speech | `pip install .[speech]` |
| Everything | `pip install .[all]` |

## Running

```bash
python chatbot_modules/main.py --text
python chatbot_modules/main.py --test
python chatbot_modules/main.py --gui
```

Or use the package interface:

```python
from chatbot.core.chatbot_core import ChatBot

bot = ChatBot()
print(bot.respond("hello!"))
```

## Offline Voice

The GUI can use Vosk for local speech recognition. A compatible Vosk model is placed under the project's model directory; if voice dependencies are unavailable, the rest of the chatbot continues to work.

## Optional LLM Layer

An LLM can act as a final fallback for messages that the deterministic/ML layers do not understand. This layer is deliberately optional rather than being the foundation of the chatbot.

API credentials should be supplied through environment variables or local ignored configuration.

## Testing

```bash
pip install -e .[dev]
pytest
```

The test suite covers core intent handling, typo correction, database behaviour, creative generators and response-bank integrity.

## Project Status

**Active development**

The project is intentionally modular and experimental. Optional capabilities may require additional dependencies or local models.

## Philosophy

The interesting part of this project is not simply generating a response. It explores how a conversational system can combine **deterministic logic, structured memory, intent recognition, local models and optional generative AI** while remaining useful when external services are unavailable.