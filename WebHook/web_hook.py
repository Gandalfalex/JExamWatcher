from flask import Flask, request, jsonify
from .telegram_bot import TelegramBot
import json
import requests
import os
from .messages import options

app = Flask(__name__)
bot = TelegramBot()
location = os.path.dirname(os.path.realpath(__file__))

@app.route('/webhook', methods=['POST'])
def index():
    '''
    what to do if there is a new message
    enter new chat id in watch list to notify others
    '''
    req = request.get_json()
    print(req)
    message = req['message']['text']
    chat_id = req['message']['chat']['id']
    name = req['message']['chat']['first_name']
    update_chat_ids(chat_id)
    if message in options:
        if message == "/remove":
            remove_chat_id(chat_id)
        message = options.get(message)

    success = bot.action(message, chat_id, False, name = str(name))

    return jsonify(success = success)

''' get's the ids of every person that will to get informed'''
def get_chat_ids():
    ids = []
    with open("{}/database/chat_ids.json".format(location)) as file:
        old_ids = json.load(file)
        for id in old_ids:
            ids.append(id)
    return ids

def update_chat_ids(id):
    ids = get_chat_ids()
    if id in ids:
        return
    else:
        ids.append(id)
        with open("{}/database/chat_ids.json".format(location), "w") as file:
            json.dump(ids, file, ensure_ascii=False, indent=4)

def remove_chat_id(id):
    ids = get_chat_ids()
    if id in ids:
        ids.remove(id)
        with open("{}/database/chat_ids.json".format(location), "w") as file:
            json.dump(ids, file, ensure_ascii=False, indent=4)
    
def send(exams):
    if len(exams) > 0:
        for i in get_chat_ids():
            for msg in exams:
                bot.action(msg, i, True)

def run_app():
    temp = requests.get("http://localhost:4040/api/tunnels")
    bot = TelegramBot()
    TelegramBot.init_webhook(temp)
    app.app_context()
    app.run(port=8080)

