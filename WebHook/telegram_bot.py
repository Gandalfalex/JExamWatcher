from telegram import Bot
import requests
from config import TOKEN, TELEGRAM_SEND_MESSAGE_URL, TELEGRAM_INIT_WEBHOOK_URL
from time import sleep
import json
import messages


class TelegramBot:

    def __init__(self):
       self.chat_id = None

    def action(self, original_message, id, reply, name = ""):
        success = None
        if reply:
            success = self.send_message(original_message.replace(',','') + " has just been released", id)
        else:
            success = self.send_message(self.create_message(original_message, name), id)
        return success

    def create_message(self, msg, name):
        if str(msg).lower() == "/start":
            return "Hello "+ name + "\n" + messages.GREETING
        elif str(msg).lower() == "/help":
            return messages.HELP
        elif str(msg).lower() == "/whoisyourdaddy":
            return messages.DADDY
        elif str(msg).lower() == "/remove":
            return messages.REMOVE
        else:
            return msg

    def send_message(self, message, id):
        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(id, message))
        return True if res.status_code == 200 else False 
 
    @staticmethod
    def init_webhook(res):
        res_unicode = res.content.decode("utf-8")
        res_json = json.loads(res_unicode)
        http_url = TELEGRAM_INIT_WEBHOOK_URL + str(res_json["tunnels"][0]["public_url"]) + '/webhook'
        requests.get(http_url)
