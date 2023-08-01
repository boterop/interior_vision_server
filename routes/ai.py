import os
from lib.gpt import GPT
from lib.dall_e import Dall_E
from flask import request, Blueprint
from lib.db import DB

ai = Blueprint('ai', __name__)

ASSISTANT_NOT_FOUND = "The assistant with id {} was not found"
SERVER_ERROR = "Internal server error"
MESSAGES_LIMIT = "You have been reached the max length of memory"
CONTEXT_LENGTH_EXCEEDED = "context_length_exceeded"


def create_new_assistant():
    role = os.getenv("DESIGNER_ROLE")
    language = get("language")
    assistant = GPT()
    assistant.set_role(role)
    assistant.set_language(language)
    assistant.set_system(os.getenv("FIRST_CONFIG"))
    return assistant


def get(prop):
    data = request.get_json(force=True)
    return data[prop]


def get_assistant(assistant_id):
    database = DB()
    assistant_memory = database.get_assistant_memory(assistant_id)
    assistant = GPT()
    assistant.set_memory(assistant_memory)
    return assistant


def response(code, message):
    return {'status': code, 'response': message}


@ai.route('/ask', methods=['POST'])
def ask():
    database = DB()
    message = get("message")
    assistant_id = get("assistant_id")

    assistant = get_assistant(assistant_id)
    try:
        resp = assistant.ask(message)
        database.save_memory(assistant_id, assistant.get_memory())
        return response(200, resp)
    except Exception as e:
        print(e)
        if e.code == CONTEXT_LENGTH_EXCEEDED:
            return response(409, MESSAGES_LIMIT)
        return response(500, SERVER_ERROR)


@ai.route('/view', methods=['POST'])
def view():
    dall_e = Dall_E()

    assistant_id = get("assistant_id")
    assistant = get_assistant(assistant_id)

    try:
        prompt = assistant.ask(os.getenv("CREATE_PROMPT")).replace("\n", ". ")
        print("{}, {}".format(prompt, os.getenv("DALLE_CONFIG")))
        url = dall_e.create_image("{}, {}".format(
            prompt, os.getenv("DALLE_CONFIG")), Dall_E.MEDIUM, 1)

        return response(200, url)
    except Exception as e:
        print(e)
        if e.code == CONTEXT_LENGTH_EXCEEDED:
            return response(409, MESSAGES_LIMIT)
        return response(500, SERVER_ERROR)


@ai.route('/create-assistant', methods=['POST'])
def create_assistant():
    database = DB()
    assistant = create_new_assistant()
    assistant_id = database.create_memory(assistant.get_memory())
    return {'status': 200, 'response': assistant_id}


@ai.route('/get-memory', methods=['POST'])
def get_memory():
    database = DB()
    assistant_id = get("assistant_id")
    try:
        assistant_memory = database.get_assistant_memory(assistant_id)
        return response(200, assistant_memory)
    except TypeError:
        return response(409, ASSISTANT_NOT_FOUND.format(assistant_id))
    except Exception:
        return response(500, SERVER_ERROR)


@ai.route('/clean-memory', methods=['POST'])
def clean_memory():
    database = DB()
    assistant_id = get("assistant_id")
    assistant = create_new_assistant()
    database.save_memory(assistant_id, assistant.get_memory())
    return response(200, assistant.get_memory())


@ai.route('/health', methods=['POST'])
def health():
    return response(200, "OK")
