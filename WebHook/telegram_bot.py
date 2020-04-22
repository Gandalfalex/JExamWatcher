import requests
from .config import TOKEN, TELEGRAM_SEND_MESSAGE_URL, TELEGRAM_INIT_WEBHOOK_URL
import json


class TelegramBot:

    def __init__(self):
       self.chat_id = None

    def action(self, original_message, id, reply, name = ""):
        success = None
        if reply:
            success = self.send_message(original_message.replace(',','') + " has just been released", id)
        else:
            success = self.send_message(original_message, id)
        return success

    def send_message(self, message, id):
        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(id, message))
        return True if res.status_code == 200 else False 
 
    @staticmethod
    def init_webhook(res):
        res_unicode = res.content.decode("utf-8")
        res_json = json.loads(res_unicode)
        http_url = TELEGRAM_INIT_WEBHOOK_URL + str(res_json["tunnels"][0]["public_url"]) + '/webhook'
        requests.get(http_url)
