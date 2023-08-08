import os
import uuid
from lib.gpt import GPT
from lib.dall_e import Dall_E
from flask import request, Blueprint
from lib.db import DB

ai = Blueprint('ai', __name__)

ASSISTANT_NOT_FOUND = "The assistant with id {} was not found"
SERVER_ERROR = "Internal server error"
UNAUTHORIZED_ERROR = "Unauthorized"
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


def is_authorized():
    return request.headers["Authorization"].split(" ")[1] == os.getenv("AUTH_KEY")


def get_assistant(assistant_id, assistant_key):
    database = DB()
    assistant_memory = database.get_assistant_memory(
        assistant_id, assistant_key)
    assistant = GPT()
    assistant.set_memory(assistant_memory)
    database.close()
    return assistant


def response(code, message):
    return {'status': code, 'response': message}


@ai.route('/ask', methods=['POST'])
def ask():
    if not is_authorized():
        return response(401, UNAUTHORIZED_ERROR)
    database = DB()
    message = get("message")
    assistant_id = get("assistant_id")
    assistant_key = get("assistant_key")

    try:
        assistant = get_assistant(assistant_id, assistant_key)
        resp = assistant.ask(message)
        database.save_memory(assistant_id, assistant_key,
                             assistant.get_memory())
        database.close()
        return response(200, resp)
    except TypeError:
        return response(409, ASSISTANT_NOT_FOUND.format(assistant_id))
    except Exception as e:
        print(e)
        if e.code == CONTEXT_LENGTH_EXCEEDED:
            return response(409, MESSAGES_LIMIT)
        return response(500, SERVER_ERROR)


@ai.route('/view', methods=['POST'])
def view():
    if not is_authorized():
        return response(401, UNAUTHORIZED_ERROR)
    dall_e = Dall_E()

    assistant_id = get("assistant_id")
    assistant_key = get("assistant_key")

    try:
        assistant = get_assistant(assistant_id, assistant_key)
        prompt = assistant.ask(os.getenv("CREATE_PROMPT")).replace("\n", ". ")
        print("{}, {}".format(prompt, os.getenv("DALLE_CONFIG")))
        url = dall_e.create_image("{}, {}".format(
            prompt, os.getenv("DALLE_CONFIG")), Dall_E.MEDIUM, 1)

        return response(200, url)
    except TypeError:
        return response(409, ASSISTANT_NOT_FOUND.format(assistant_id))
    except Exception as e:
        print(e)
        if e.code == CONTEXT_LENGTH_EXCEEDED:
            return response(409, MESSAGES_LIMIT)
        return response(500, SERVER_ERROR)


@ai.route('/create-assistant', methods=['POST'])
def create_assistant():
    if not is_authorized():
        return response(401, UNAUTHORIZED_ERROR)
    database = DB()
    free_assistant = database.get_free_assistant()
    assistant = create_new_assistant()
    assistant_key = str(uuid.uuid4())

    if (free_assistant is None):
        assistant_id = database.create_memory(
            assistant_key, assistant.get_memory())
    else:
        assistant_id = free_assistant[0]
        database.update_key(assistant_id, assistant_key)
        database.save_memory(assistant_id, assistant_key,
                             assistant.get_memory())

    database.close()

    return response(200, {'assistant_id': assistant_id, 'assistant_key': assistant_key})


@ai.route('/get-memory', methods=['POST'])
def get_memory():
    if not is_authorized():
        return response(401, UNAUTHORIZED_ERROR)
    database = DB()
    assistant_id = get("assistant_id")
    try:
        assistant_key = get("assistant_key")
        assistant_memory = database.get_assistant_memory(
            assistant_id, assistant_key)
        database.close()
        return response(200, assistant_memory)
    except (TypeError, KeyError):
        return response(409, ASSISTANT_NOT_FOUND.format(assistant_id))
    except Exception as e:
        print(e)
        return response(500, SERVER_ERROR)


@ai.route('/clean-memory', methods=['POST'])
def clean_memory():
    if not is_authorized():
        return response(401, UNAUTHORIZED_ERROR)
    database = DB()
    assistant_id = get("assistant_id")
    assistant_key = get("assistant_key")
    assistant = create_new_assistant()
    database.save_memory(assistant_id, assistant_key, assistant.get_memory())
    database.close()
    return response(200, assistant.get_memory())


@ai.route('/health', methods=['GET'])
def health():
    return response(200, "OK")
