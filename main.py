from flask import Flask, request, jsonify, Response, send_from_directory
import json
import vonage
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Environment Variables
VONAGE_APPLICATION_ID = os.getenv('VONAGE_APPLICATION_ID')
API_KEY_PATH = os.getenv('API_KEY_PATH')
TO_NUMBER = os.getenv('TO_NUMBER')
VONAGE_NUMBER = os.getenv('VONAGE_NUMBER')

# Vonage Client Setup
client = vonage.Client(
    application_id=VONAGE_APPLICATION_ID,
    private_key=API_KEY_PATH,
)

server_remote_url = "https://d805-2603-6080-5a03-db44-f15a-4024-8474-e8a9.ngrok-free.app/"

# Define the path to your MP3 file and its directory
AUDIO_FILE_PATH = '/Users/ryanhuang/Documents/GitHub/live-voice/audio_files'
AUDIO_FILE_NAME = '127b95ac-dcec-497f-a9a8-f753d3940d8c.mp3'

@app.route('/hello-audio')
def serve_audio():
    """
    Serve the MP3 audio file.
    """
    return send_from_directory(AUDIO_FILE_PATH, AUDIO_FILE_NAME)

@app.route('/webhooks/answer', methods=['GET'])
def answer_call():
    ncco = [
        {
            'action': 'stream',
            "streamUrl": ["https://d805-2603-6080-5a03-db44-f15a-4024-8474-e8a9.ngrok-free.app/hello-audio"],
            "bargeIn": "true"
        },
        {
            'action': 'input',
            'eventUrl': [f"{server_remote_url}webhooks/input"],
            'type': ['speech'],
            'speech': {
                'uuid': [request.args.get('uuid')],
                'endOnSilence': 3,
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
    print("Input received:", request.json)
    speech_results = request.json.get('speech', {}).get('results', [])
    response_text = 'You said nothing recognizable.' if not speech_results else f'You said: {speech_results[0].get("text")}. Please say something else.'
    response_ncco = [
        {'action': 'talk', 'text': response_text},
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
    app.run(port=5000)
