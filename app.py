import os
import re

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests


# Install the Slack app and get xoxb- token in advance
app = App(token="xoxb-336488795315-7637665953460-YOdzYLO1rMiEb38fduIx07GD")
client = WebClient(token="xoxb-336488795315-7637665953460-YOdzYLO1rMiEb38fduIx07GD")

@app.command("/hello-socket-mode")
def hello_command(ack, body):
    user_id = body["user_id"]
    ack(f"Hi, <@{user_id}>!")

@app.event("app_mention")
def event_test(event, say):
    # Print the message text to the log
    text = event.get('text')
    channel = event.get('channel')
    ts = event.get('ts')
    print(f"App mentioned in channel {channel}: {text} and the ts of msg is : {ts}")
    try:
        # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel = channel,
            thread_ts = ts,
            text= "I am currently working on retrieving the answer for your question, please wait a moment...",
        )
        print(result)

    except SlackApiError as e:
        print(e)

    # Extract the question by removing the bot mention
    # The mention is usually in the form <@BOTID>
    question = re.sub(r"<@[^>]+>\s*", "", text).strip()
    print(f"Extracted question: {question}")

    url = "https://aiplatform.dev51.cbf.dev.paypalinc.com/byoa/orch-varvenkate-71672/api/v1/infer/a3bb9330-6b83-43b9-b8bb-65d268483af4"
    headers = {
        "Content-Type": "application/json",
        "X-UserID": "varvenkatesh"
    }
    payload = {
        "inputs": {
            "Chat Input": question
        }
    }
    # Make POST request
    response = requests.post(url, headers=headers, json=payload)
    # Print response
    response_json = response.json()
    answer = response_json["outputs"][0]["outputs"][0]["Chat Output"]
    try:
        # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel = channel,
            thread_ts = ts,
            markdown_text = answer
        )
        print(result)

    except SlackApiError as e:
        print(e)

if __name__ == "__main__":
    SocketModeHandler(app, "xapp-1-A07JRK92ZU4-9192921111508-5221619a803dbebc2fa0730d9bb078780453d8e273714dc1804ce2cf1f53855e").start()
