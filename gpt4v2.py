from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
from PIL import Image

load_dotenv()

NEON_GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET_COLOR = '\033[0m'

api_key = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=api_key)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def ask_about_image(image_path, question):
    # Encode the image
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                ],
            }
        ],
        max_tokens=1000,
    )
    return response.choices[0].message.content

def open_image(image_path):
    try:
        image = Image.open(image_path)
        image.show()
    except IOError:
        print(f"Unable to open the image: {image_path}")

# Path to your local image file
image_path = "C:/Users/kris_/Python/gpt4v2/image/scene.png"

# Open the image
open_image(image_path)

# Ask a question about the image
user_question = input(f"{YELLOW}Ask a question about the image: {RESET_COLOR}")
question_response = ask_about_image(image_path, user_question)
print("\nQuestion Response:")
print(NEON_GREEN + question_response + RESET_COLOR)