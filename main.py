from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from waitress import serve
from routes.ai import ai
from routes.ai_test import ai_test

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(ai)
app.register_blueprint(ai_test)

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
