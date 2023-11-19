from flask import Flask, render_template, request, jsonify
import requests


RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"
app = Flask(__name__)

# Define the URL of the Rasa API endpoint

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Get the user's message from the request
    user_message = request.form['user_message']

    # Create a payload to send to the Rasa API
    payload = {
        "sender": "user",
        "message": user_message
    }

    # Send a POST request to the Rasa API
    response = requests.post(RASA_API_URL, json=payload)

    # Parse the response from Rasa
    rasa_response = response.json()

    # Extract the bot's reply from the response
    bot_reply = rasa_response[0]['text']

    return jsonify({'bot_reply': bot_reply})

@app.route('/webhook', methods=["POST"])
def webhook():
    user_message = request.json["message"]
    print("User Message:", user_message)

    rasa_response = requests.post(RASA_API_URL, json={'message': user_message})
    rasa_response_json = rasa_response.json()

    print("RAsa Response:", rasa_response_json)

    bot_response = rasa_response_json[0]['text'] if rasa_response_json else 'Sorry, I didn\'t Understand that.'

    return jsonify ({'response': bot_response})

if __name__ == "__main__":
    app.run(debug=True, port=3000)
