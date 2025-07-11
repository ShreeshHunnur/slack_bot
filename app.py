from flask import Flask, request
from slack_sdk import WebClient
import requests
import os


app = Flask(__name__)

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")  # Replace with your bot token

client = WebClient(token=SLACK_BOT_TOKEN)

url = "https://aiplatform.dev51.cbf.dev.paypalinc.com/byoa/orch-sgundopant-434d2/api/v1/infer/8903d459-d249-49fb-883f-c3ee6aa42110"
headers = {
    "Content-Type": "application/json",
    "X-UserID": "varvenkatesh"
}

@app.route('/', methods=['POST','GET'])
def slack_events():

    if request.method == 'GET':
        return "Slack Bot is running", 200
    print(request)
    data = request.json

    # Slack URL verification challenge
    if data and data.get('type') == 'url_verification':
        print("URL,verification "+ data.get('challenge'))
        return data.get('challenge'),200

    # Handle app_mention event
    if data and 'event' in data and data['event']['type'] == 'app_mention':
        channel_id = data['event']['channel']
        text = data['event']['text']

        # Optionally, remove bot mention from text
        # text = text.replace(f"<@{your_bot_user_id}>", "").strip()

        # Prepare payload
        payload = {
            "inputs": {
                "Chat Input": text
            }
        }
        # Make POST request
        response = requests.post(url, headers=headers, json=payload)
        # Print response
        response_json = response.json()
        answer = response_json["outputs"][0]["outputs"][0]["Chat Output"]


        # Post the result back to Slack channel
        client.chat_postMessage(channel=channel_id, text=answer)

    return '', 200

if __name__ == "__main__":
    app.run(port=5000)