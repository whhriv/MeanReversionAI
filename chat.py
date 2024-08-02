import openai
import os
# Replace with your OpenAI API key

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

def chat_with_me():
  """Starts a chat session with the OpenAI API."""

  while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
      break

    response = openai.completions.create(
      model="gpt-4.0",
      messages=[
        {"role": "user", "content": user_input}
      ]
    )

    print(f"ChatGPT: {response['choices'][0]['message']['content']}")

if __name__ == "__main__":
    chat_with_me()