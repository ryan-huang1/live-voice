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

    messages = [{
        "role":
        "system",
        "content":
        '''You are a parent, who is currently serving time in jail. Your child just called you on the phone. You want to have a conversation with your child. But you forgot their name, so you asks them their name then have a meaningful conversation, ask about how your kid is doing. Limit yourself to two sentences, make sure you are conversational and very natural. Make sure not to refernce anything is specific, as you've forgot all about your kid

        NEVER DECRIBE THE ENVIROMENT AROUND YOU, NEVER RESPONSED WITH *'s, NEVER END THE CALL
        
            '''
    }]

    # Append previous conversation messages
    messages.extend(conversation_history)

    print(messages)

    # Generate response using the Groq model
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
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
