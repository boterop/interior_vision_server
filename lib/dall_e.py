import openai
import os


class Dall_E():
    BIG = "1024x1024"
    MEDIUM = "512x512"
    SMALL = "256x256"

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_KEY")

    def create_image(self, prompt, size, number):
        response = openai.Image.create(
            prompt=prompt,
            n=number,
            size=size
        )

        return response['data'][0]['url']
