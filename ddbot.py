'''DeeDee chatbot'''

from flask import Flask, request, jsonify, json
from ciscosparkapi import CiscoSparkAPI, Webhook
from jsondata import JsonData
from chatbot import Chatbot
from datetime import datetime
import json
import apiai
import threading
import os

#pylint: disable=C0103
#bot_id = api.people.me().id
path = '/'
port = '5000'
bot_token = os.environ['SPARK_TOKEN']
print(bot_token)
app = Flask(__name__)
bot = Chatbot(bot_token)
started = datetime.now()
ai_token = os.environ['APIAI_TOKEN']
print(ai_token)
ai = apiai.ApiAI(ai_token)
#pylint: enable=C0103



def initialize_environment():
    """initialize the global variables"""
    # TODO add bot initialization based on configuration
    # configuration contains:
    # - port, path, token, secret, trimMention, ignoreSelf
    # get information on self
    # register bot webhooks
    #
    return ""


@app.route(path, methods=['GET', 'POST'])
def api_root():
    if request.method == 'GET':
        response = {
            'message': 'Cisco Spark bot is up and running',
            'started': str(started),
            'path': path,
            'token': "................" + bot.get_id()[-10:]
        }
        return jsonify(response)
    elif request.method == 'POST':
        hook = Webhook(request.json)
        print('launch on_hook thread')
        thread = threading.Thread(target=bot.on_hook, args=[hook])
        thread.daemon = True
        thread.start()
        print('send response to Spark Cloud')
        response = 'Seems to be ok'
        return response

def ask_ai(message):
    ai_request = ai.text_request()
    ai_request.session_id = "444444"
    ai_request.query = message
    response = ai_request.getresponse()
    ai_obj = JsonData(json.loads(response.read().decode()))
    return ai_obj.result.fulfillment.messages[0].get('speech')

def received_message(hook: Webhook):
    print('message created')
    #print(hook.data)

def added_to_room(hook: Webhook):
    print('bot added to room')
    bot.reply(hook, "Hi there! I'm DeeDee. Thank you for adding me to your room")
    #print(hook.data)

def message_to_bot(hook: Webhook):
    print('message to me')
    print('asking ai...')
    reply = ask_ai(bot.get_message(hook))    
    bot.reply(hook, reply)
    #print(hook.data)

bot.on_event.add_handler("messages/created", received_message)
bot.on_event.add_handler("memberships/created", added_to_room)
bot.on_message += message_to_bot

if __name__ == '__main__':
    print("Starting Chatbot")
    app.run(host='0.0.0.0')
    print('Stopping chatbot')
