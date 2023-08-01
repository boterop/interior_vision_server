from flask import request, Blueprint

ai_test = Blueprint('ai_test', __name__)

ASSISTANT_NOT_FOUND = "The assistant with id {} was not found"
SERVER_ERROR = "Internal server error"
MESSAGES_LIMIT = "You have been reached the max length of memory"
CONTEXT_LENGTH_EXCEEDED = "context_length_exceeded"


def get(prop):
    data = request.get_json(force=True)
    return data[prop]


def response(code, message):
    return {'status': code, 'response': message}


@ai_test.route('/test/ask', methods=['POST'])
def test_ask():
    message = get("message")
    return response(200, message)


@ai_test.route('/test/view', methods=['POST'])
def test_view():
    return response(200, "https://www.boterop.io/documents/image.jpg")


@ai_test.route('/test/create-assistant', methods=['POST'])
def test_create_assistant():
    return response(200, "1")


@ai_test.route('/test/get-memory', methods=['POST'])
def test_get_memory():
    assistant_id = get("assistant_id")

    if assistant_id == "1":
        assistant_memory = [
            {"content": "Test content", "role": "system"},
            {"content": "Another test content", "role": "system"},
            {"content": "Third content", "role": "system"},
            {"content": "hi", "role": "user"},
            {"content": "hi", "role": "assistant"}]
        return response(200, assistant_memory)
    elif assistant_id == "2":
        return response(409, ASSISTANT_NOT_FOUND.format(assistant_id))
    else:
        return response(500, SERVER_ERROR)


@ai_test.route('/test/clean-memory', methods=['POST'])
def test_clean_memory():
    return response(200, [])


@ai_test.route('/test/health', methods=['POST'])
def test_health():
    return response(200, "OK")
