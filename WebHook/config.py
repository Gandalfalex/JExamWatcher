TOKEN = ''
BASE_TELEGRAM_URL = 'https://api.telegram.org/bot{}'.format(TOKEN)
TELEGRAM_INIT_WEBHOOK_URL = '{}/setWebhook?url='.format(BASE_TELEGRAM_URL)
TELEGRAM_SEND_MESSAGE_URL = BASE_TELEGRAM_URL + '/sendMessage?chat_id={}&text={}'
