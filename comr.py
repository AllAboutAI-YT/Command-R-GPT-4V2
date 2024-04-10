import cohere
from dotenv import load_dotenv
import os

load_dotenv()
NEON_GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET_COLOR = '\033[0m'
api_key = os.getenv("COMMAND_R_API_KEY")
co = cohere.Client(api_key)

def ask_question(question, chat_history):
    response = co.chat(
        chat_history=chat_history,
        message=question,
        connectors=[{"id": "web-search"}]
    )

    answer_text = response.text
    citation_urls = [doc['url'] for doc in response.documents]

    print(NEON_GREEN + "Answer:" + RESET_COLOR)
    print(answer_text)
    print()
    print(CYAN + "Citations:" + RESET_COLOR)
    for url in citation_urls:
        print(url)
    print()

    return response.text

def main():
    chat_history = []

    while True:
        user_input = input(YELLOW + "Ask a question (or type 'quit' to exit): " + RESET_COLOR)
        if user_input.lower() == 'quit':
            break

        chat_history.append({"role": "USER", "message": user_input})
        answer = ask_question(user_input, chat_history)
        chat_history.append({"role": "CHATBOT", "message": answer})

if __name__ == '__main__':
    main()