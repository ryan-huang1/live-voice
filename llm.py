import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize the Groq client with API key
API_KEY = os.getenv('API_KEY')
client = Groq(api_key=API_KEY)

def get_groq_response(conversation_history):
    """Function to get a response from Groq client based on user's question within the context of the conversation history."""

    messages = [
        {
            "role": "system",
            "content": "Your name is Mr. Ingram. You are a teacher, but also a bit snarky and never that excited about things. Limit yourself to 2 sentences per response. Make sure not to use markdown asterisks, and don't say things like sigh. Only plain sentences"
        }
    ]

    # Append previous conversation messages
    messages.extend(conversation_history)

    # Generate response using the Groq model
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=1,
        max_tokens=100,
        top_p=1,
        stream=False,
        stop=None,
    )

    # Assuming that the Groq model response is structured similarly to the OpenAI's API
    return completion.choices[0].message.content

# Example usage:
question = "Hi, how are you doing today?"
# response = get_groq_response(question)
# print(response)
