Offline Multilingual Chatbot
An offline-first chatbot that speaks English, Swahili, and French, mixing a rule-based intent engine with optional ML backends (scikit-learn, PyTorch/Keras) and an optional LLM fallback (Claude or GPT) for anything its fixed vocabulary doesn't cover. Originally built as a single script for Pydroid 3 on Android; still runs there unchanged.
Features
Conversation: greetings, small talk, tone tracking, memory of facts/name/birthday you tell it, typo correction.
Creative writing: stories, poems, haiku, acrostics, jokes, quotes, riddles, ASCII art, fantasy names.
Games: rock-paper-scissors, tic-tac-toe, hangman, dice/coin, word scramble, flashcards, trivia, anagrams.
Tools: math, unit/currency conversion, text tools, ciphers, password/hash/base64, QR codes, to-dos, countdowns, weather, news, markdown tables, tipping.
ML backends: intent/sentiment classifiers, mood forecasting, semantic memory search - falls back gracefully to rule-based behavior if scikit-learn/PyTorch/Keras aren't installed.
Vision: image analysis, face blurring, style transfer, shape classification (needs numpy/Pillow/OpenCV).
LLM bridge: optional last-resort fallback to Claude or GPT for messages nothing else understood - opt-in, never required.
Requirements
Python 3.9+
No required third-party packages for the core CLI path (--text, --test) - everything else is an optional extra (see below).
Feature
Install with
GUI (Kivy)
pip install .[gui]
Vision
pip install .[vision]
Classical ML
pip install .[ml]
Deep learning (PyTorch)
pip install .[ml-torch]
Offline voice input
pip install .[speech]
Everything
pip install .[all]
Voice input (offline, via Vosk)
The GUI's mic button uses Vosk for fully offline speech-to-text - no cloud API, no internet needed at runtime, matching the app's offline-first design. Setup:
pip install .[speech]
Download a model from https://alphacephei.com/vosk/models (e.g. vosk-model-small-en-us-0.15 for a small, fast English model)
Extract it into chatbot_modules/vosk_model/ (a folder, not a file)
If the model or a working microphone backend isn't found, the mic button explains what's missing instead of silently failing - no setup is required for the rest of the app to work.
Installation
Pydroid 3 / Android: open chatbot_modules/main.py in Pydroid 3 and tap Run. This mode execs the numbered files directly and needs no pip install step - see that file's docstring for why it's built this way.
Desktop / anywhere else:
git clone <this repo>
cd <this repo>
pip install -e .[all]        # or a narrower extra, see table above
python chatbot_modules/main.py --text      # plain-text chat
python chatbot_modules/main.py --test      # self-test + accuracy harness
python chatbot_modules/main.py --gui       # Kivy GUI (needs [gui])
Or, using the installed package directly:
from chatbot.core.chatbot_core import ChatBot
bot = ChatBot()
print(bot.respond("hello!"))
Configuration
LLM and translation settings live in two JSON files next to the numbered modules: chatbot_llm_config.json and chatbot_translation_config.json. Neither is committed (see .gitignore) - copy the matching *.example.json file to the real name and fill in your key, or skip the file entirely and set an environment variable instead:
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
# LIBRETRANSLATE_API_KEY also supported
An environment variable always overrides whatever is in the JSON file. Both are optional - the bot works fully offline without either.
Switching providers mid-conversation: the LLM config stores anthropic_api_key and openai_api_key as two separate fields, so if you set both ahead of time (via the JSON file or both env vars), saying "change to gpt" or "change to claude" in chat switches instantly with no re-entry needed. If only one is set, switching to the other will tell you it's missing a key rather than silently failing.
Architecture overview
chatbot_modules/main.py exec()s ~52 numbered files, in a fixed order, into one shared namespace - a deliberate trade-off for Pydroid 3 (see that file's docstring), not an accident. Two things build on top of that flat folder without changing it:
src/chatbot/ - a real, pip install-able package that gives every file a clean dotted import path (chatbot.nlp.intent_engine, chatbot.core.chatbot_core, ...), backed by the exact same source files in chatbot_modules/ (no duplication). See src/chatbot/_bootstrap.py for exactly how and why.
ChatBot itself (14_chatbot_core.py) is composed rather than monolithic: SystemHandlers, CreativeHandlers, GameHandlers, MemoryHandlers, and ToolHandlers each own a themed slice of what used to be ~172 methods on one class, with ChatBot reduced to orchestration (intent registration, dispatch, shared helpers).
Response-bank data (phrase variants per intent, files 33-52) makes up the large majority of the codebase's line count and is disclosed, auto-templated data, not logic.
Supported languages
English (en), Swahili (sw), and French (fr) - coverage varies by feature; response banks are the most complete, some tool output (e.g. generated passwords, QR payloads) is language-independent by nature.
Running tests
pip install -e .[dev]
pytest
Covers the intent engine/typo corrector, the database layer, creative writing generators, and response-bank data integrity (every bank has all three language keys, non-empty). See tests/.
Contributing / extending
To add a new intent:
Add the handler method to whichever composed group fits (SystemHandlers, CreativeHandlers, GameHandlers, MemoryHandlers, ToolHandlers - or ChatBot itself only for genuine orchestration).
Register it in ChatBot._register_intents() the same way existing intents are registered - self._handle_your_new_thing resolves correctly regardless of which group actually owns it.
Add a case to chatbot_modules/21_main_and_tests.py's ACCURACY_TEST_CASES and, if it's a self-contained piece, a pytest test under tests/.
