from flask import Flask, request, jsonify
from telegram_bot import TelegramBot
import json
import requests
from enum import Enum
import os


class MessageType(Enum):
    IMG = 1
    DOC = 2
    MSG = 3
    NONE = 4 


app = Flask(__name__)
bot = TelegramBot()
location = os.path.dirname(os.getcwd())

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
    
    # type_of_file = None
    # if req['message'].get('text') != None:
    #     type_of_file = MessageType.MSG
    #     message = req['message']['text']
    # elif req['message'].get('photo') != None:
    #     type_of_file = MessageType.IMG
    # elif req['message'].get('document') != None:
    #     type_of_file = MessageType.DOC

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
    
def send(exams):
    if exams != None:
        for i in get_chat_ids():
            for msg in exams:
                success = bot.action(msg, i, True)
        return "200"
    else:
        return "404" 

def run_app():
    temp = requests.get("http://localhost:4040/api/tunnels")
    TelegramBot.init_webhook(temp)
    app.app_context()
    app.run(port=8080)


def crap():
    return 2

if __name__ == '__main__':
    run_app()
   
