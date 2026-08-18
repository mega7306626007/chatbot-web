import os
import threading

from flask import Flask, render_template, request, jsonify

# Skip the CLI/--test/--gui dispatch at the bottom of chatbot.py entirely -
# only need the ChatBot class itself here.
import importlib.util

_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "chatbot_module", os.path.join(_HERE, "chatbot.py")
)
chatbot_module = importlib.util.module_from_spec(_spec)
# A non-"__main__" name means the `if __name__ == "__main__":` block at
# the bottom of chatbot.py never fires, so no CLI/GUI ever tries to launch.
_spec.loader.exec_module(chatbot_module)

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Build ChatBot() in a background thread instead of at module level.
# Render's free tier cancels a deploy if it can't detect an open port within
# a few minutes - constructing ChatBot() (parsing/compiling a 25k-line file,
# initializing the database, fitting the TF-IDF matcher, etc.) was taking
# longer than that window, so the port never got a chance to open at all.
# Starting Flask immediately and loading the bot afterward, in parallel,
# fixes that: the port opens right away, and requests that arrive before
# the bot is ready just get a short "still starting up" reply instead of
# the whole deploy timing out.
# ---------------------------------------------------------------------------
_bot_holder = {"bot": None, "error": None}


def _load_bot_in_background():
    try:
        _bot_holder["bot"] = chatbot_module.ChatBot()
    except Exception as exc:
        _bot_holder["error"] = exc
        app.logger.exception("Failed to initialize ChatBot")


threading.Thread(target=_load_bot_in_background, daemon=True).start()


def get_response(message: str) -> str:
    bot = _bot_holder["bot"]
    if bot is None:
        if _bot_holder["error"] is not None:
            raise _bot_holder["error"]
        return "I'm still starting up - please try again in a few seconds."
    return bot.respond(message)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message."}), 400

    try:
        reply = get_response(user_message)
    except Exception:
        app.logger.exception("Chatbot failed to generate a reply")
        reply = "Sorry, something went wrong on my end. Please try again."

    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False, load_dotenv=False)