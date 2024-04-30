import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize the Groq client with API key
API_KEY = os.getenv('API_KEY')
client = Groq(api_key=API_KEY)

def get_groq_response(user_question):
    """Function to get response from Groq client based on user's question."""
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "Your name is Mr. Ingram. You are a teacher, but also a bit snarky and never that excited about things. Limit yourself to 2 sentences per response."
            },
            {
                "role": "user",
                "content": user_question
            },
        ],
        temperature=1,
        max_tokens=100,
        top_p=1,
        stream=False,
        stop=None,
    )
    return completion.choices[0].message.content

# Example usage:
question = "Hi, how are you doing today?"
# response = get_groq_response(question)
# print(response)
