import os
from lib.gpt import GPT
from lib.dall_e import Dall_E
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from lib.db import DB
from waitress import serve

load_dotenv()

app = Flask(__name__)
CORS(app)


def get(prop):
    data = request.get_json(force=True)
    return data[prop]


def get_assistant(assistant_id):
    assistant_memory = DB.get_assistant_memory(assistant_id)
    assistant = GPT()
    assistant.set_memory(assistant_memory)
    return assistant


def response(code, message):
    return {'status': code, 'response': message}


@app.route('/ask', methods=['POST'])
def ask():
    message = get("message")
    assistant_id = get("assistant_id")

    assistant = get_assistant(assistant_id)
    resp = assistant.ask(message)
    DB.save_memory(assistant_id, assistant.get_assistant_memory())
    return response(200, resp)


@app.route('/view', methods=['POST'])
def view():
    role_prompt = os.getenv("PROMPT_ROLE")
    gpt_prompt = GPT()
    gpt_prompt.set_role(role_prompt)
    dall_e = Dall_E()

    assistant_id = get("assistant_id")
    assistant = get_assistant(assistant_id)

    last_result = assistant.get_last_said()
    prompt = gpt_prompt.ask(last_result).replace("\n", ". ")
    url = dall_e.create_image(prompt, Dall_E.BIG, 1)

    return response(200, url)


@app.route('/create-assistant', methods=['POST'])
def create_assistant():
    role = os.getenv("DESIGNER_ROLE")
    language = get("language")
    assistant = GPT()
    assistant.set_role(role)
    assistant.set_language(language)
    resp = assistant.ask(os.getenv("FIRST_CONFIG"))
    assistant_id = DB.create_memory(assistant.get_memory())
    return {'status': 200, 'assistant_id': assistant_id, 'response': resp}


@app.route('/get-memory', methods=['POST'])
def get_memory():
    assistant_id = get("assistant_id")
    assistant = get_assistant(assistant_id)
    return response(200, assistant.get_memory)


@app.route('/health', methods=['POST'])
def health():
    return response(200, "OK")


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=6000)

# role = os.getenv("DESIGNER_ROLE")
# role_prompt = os.getenv("PROMPT_ROLE")

# gpt = GPT(role)
# gpt_prompt = GPT(role_prompt)
# dall_e = Dall_E()

# last_result = gpt.ask(os.getenv("FIRST_CONFIG"))

# while (last_result != "ya"):
#     print(last_result)
#     last_result = gpt.ask(input())

# print(last_result)

# prompt = gpt_prompt.ask(last_result).replace("\n", ". ")

# print("prompt: {}".format(prompt))
# url = dall_e.create_image(prompt, Dall_E.BIG, 1)

# print(url)
