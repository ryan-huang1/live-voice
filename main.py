from flask import Flask, request, jsonify, Response, send_from_directory
import json
import vonage
from dotenv import load_dotenv
from llm import get_groq_response
from helper import manage_chat_history, get_chat_history
import os
from voice import generate_audio_file  # Importing from 11labs.py

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Environment Variables
VONAGE_APPLICATION_ID = os.getenv('VONAGE_APPLICATION_ID')
API_KEY_PATH = os.getenv('API_KEY_PATH')
TO_NUMBER = os.getenv('TO_NUMBER')
VONAGE_NUMBER = os.getenv('VONAGE_NUMBER')
AUDIO_FILE_PATH = os.getenv('AUDIO_FILE_PATH')
server_remote_url = os.getenv('SERVER_REMOTE_URL')

# Vonage Client Setup
client = vonage.Client(
    application_id=VONAGE_APPLICATION_ID,
    private_key=API_KEY_PATH,
)

@app.route('/hello-audio/<filename>')
def serve_audio(filename):
    """
    Serve the dynamically generated MP3 audio file.
    """
    return send_from_directory(AUDIO_FILE_PATH, filename)

@app.route('/webhooks/answer', methods=['GET'])
def answer_call():
    # Logging the request details
    print("Received GET request for /webhooks/answer")

    text_to_convert = "Hi i'm mr ingram, lets have a conversation!!"
    audio_filename = generate_audio_file(text_to_convert, AUDIO_FILE_PATH)
    audio_url = f"{server_remote_url}hello-audio/{audio_filename}"

    ncco = [
        {
            'action': 'stream',
            "streamUrl": [audio_url],
            "bargeIn": "true"
        },
        {
            'action': 'input',
            'eventUrl': [f"{server_remote_url}webhooks/input"],
            'type': ['speech'],
            'speech': {
                'uuid': [request.args.get('uuid')],
                'endOnSilence': 1,
                'language': 'en-US'
            }
        }
    ]
    return Response(json.dumps(ncco), mimetype='application/json')

@app.route('/webhooks/event', methods=['POST'])
def events():
    print("Event received:", request.json)
    return "OK", 200

@app.route('/webhooks/input', methods=['POST'])
def handle_input():
    input_data = request.json
    print("Input received:", input_data)
    uuid = input_data.get('uuid', 'No UUID found')
    print("UUID:", uuid)

    # Extracting the highest confidence result text
    speech_results = input_data.get('speech', {}).get('results', [])
    if speech_results:
        highest_confidence_result = max(speech_results, key=lambda result: result.get('confidence', 0))
        user_text = highest_confidence_result.get('text', '')
        manage_chat_history(uuid, user_text, "user")
    else:
        user_text = "Call ended"
        manage_chat_history(uuid, user_text, "vonage")

    # Get system response
    system_response = get_groq_response(get_chat_history(uuid))
    manage_chat_history(uuid, system_response, "assistant")

    audio_filename = generate_audio_file(system_response, AUDIO_FILE_PATH)
    audio_url = f"{server_remote_url}hello-audio/{audio_filename}"
    response_ncco = [
        {
            'action': 'stream',
            "streamUrl": [audio_url],
            "bargeIn": "true"
        },
        {
            'action': 'input',
            'eventUrl': [f"{server_remote_url}webhooks/input"],
            'type': ['speech'],
            'speech': {
                'uuid': [request.json['uuid']],
                'endOnSilence': 3,
                'language': 'en-US'
            }
        }
    ]
    return jsonify(response_ncco)

@app.route('/make-call', methods=['GET'])
def make_call():
    response = client.voice.create_call({
        'to': [{'type': 'phone', 'number': TO_NUMBER}],
        'from': {'type': 'phone', 'number': VONAGE_NUMBER},
        'answer_url': [f"{server_remote_url}webhooks/answer"]
    })
    # Extract the UUID from the response and print it
    uuid = response['uuid']
    print(uuid)
    return f"Call initiated with UUID: {uuid}", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
