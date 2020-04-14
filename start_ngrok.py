import subprocess as sub
from time import sleep
from WebHock.web_hook import run_app
import requests

def open_ngrok():
    temp = None
    try: 
        temp = requests.get("http://localhost:4040/api/tunnels")
        if temp.status_code.__eq__(200):
            print("online")
            return True
    except requests.exceptions.ConnectionError:
        sleep(5)
        sub.Popen(['./ngrok', 'http', '8080'], stdout = sub.DEVNULL)
        sleep(10)
        temp = requests.get("http://localhost:4040/api/tunnels")
        if temp.status_code.__eq__(200):
            return True
        return False


if __name__ == "__main__":
    if open_ngrok():
        sleep(20)
        run_app()
    

