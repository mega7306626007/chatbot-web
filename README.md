# Offline Multilingual Chatbot

> A modular Python chatbot with offline-first conversation, multilingual support, games, tools, memory, optional ML, and optional LLM fallback.

This project grew from a lightweight Android/Pydroid chatbot into a modular Python system with a clear separation between conversational handlers, intent processing, memory, tools, and optional intelligence backends.

## Highlights

- 🌍 English, Kiswahili, and French
- 🧠 Rule-based intent engine with optional ML backends
- 💬 Conversation memory and tone tracking
- ✍️ Creative writing: poems, stories, jokes, riddles and more
- 🎮 Games and learning utilities
- 🧰 Math, conversions, text tools, QR generation and other utilities
- 👁️ Optional computer-vision features
- 🎙️ Offline voice input through Vosk
- 🧩 Optional PyTorch/Keras/scikit-learn integrations
- 🔌 Optional Claude/GPT fallback — never required for core operation
- 📱 Designed to retain an offline path for Android/Pydroid 3

## Architecture

The project has two complementary entry points:

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

The numbered-module structure is deliberate: it preserves the original Pydroid 3 execution model. The `src/chatbot` package provides a cleaner installable interface without duplicating the underlying source.

## Design

The chatbot is composed rather than treated as one giant conversational class. The major handler groups cover:

- System behaviour
- Creative generation
- Games
- Memory
- Tools

Response-bank files contain multilingual response data and account for a large part of the repository size; they are data, not equivalent amounts of application logic.

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

## Extending the Bot

To add an intent:

1. Put the handler in the appropriate composed handler group.
2. Register the intent in the chatbot's intent registry.
3. Add accuracy cases.
4. Add a focused automated test where appropriate.
5. Add multilingual response data when the feature requires it.

## Project Status

🚧 **Active development**

The project is intentionally modular and experimental. Optional capabilities may require additional dependencies or local models.

## Philosophy

The interesting part of this project is not simply generating a response. It explores how a conversational system can combine **deterministic logic, structured memory, intent recognition, local models and optional generative AI** while remaining useful when external services are unavailable.
