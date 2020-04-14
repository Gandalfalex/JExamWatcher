from WebHook.web_hook import send
import jexamScanner

if __name__ == "__main__":
   temp = jexamScanner.generate_data()
   send(temp)
   
