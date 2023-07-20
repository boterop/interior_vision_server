import openai
import os


class GPT():
    def __init__(self, role):
        openai.api_key = os.getenv("OPENAI_KEY")
        self.messages = [{"role": "system", "content": role}]

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_KEY")

    def memorize(self, text):
        self.messages.append({"role": "assistant", "content": text})

    def get_memory(self):
        return self.messages

    def set_memory(self, memory):
        self.messages = memory

    def get_last_said(self):
        return self.messages[-1]["content"]

    def ask(self, text):
        self.messages.append({"role": "user", "content": text})

        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        ).choices[0].message.content

        self.memorize(result)

        return result