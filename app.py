import os

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

bot = chatbot_module.ChatBot()  # loads once, at server startup


def get_response(message: str) -> str:
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
