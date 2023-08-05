import requests
from os import getenv
from urllib.parse import quote


"""
You should first configure CallMeBot as explained at https://www.callmebot.com/
"""


whatsapp_phone = getenv('CALLMEBOT_WHATSAPP_PHONE')
whatsapp_apikey = getenv('CALLMEBOT_WHATSAPP_APIKEY')
signal_phone = getenv('CALLMEBOT_SIGNAL_PHONE')
signal_apikey = getenv('CALLMEBOT_SIGNAL_APIKEY')
telegram_username = getenv('CALLMEBOT_TELEGRAM_USERNAME')


def whatsapp(message: str) -> str:
    """Send a Whatsapp message."""

    assert whatsapp_phone is not None
    assert whatsapp_apikey is not None

    text = quote(message)
    url = f'https://api.callmebot.com/whatsapp.php?phone={whatsapp_phone}&apikey={whatsapp_apikey}&text={text}'
    return requests.get(url).text


def signal(message: str) -> str:
    """Send a Signal message."""

    assert signal_phone is not None
    assert signal_apikey is not None

    text = quote(message)
    url = f'https://api.callmebot.com/signal.php?phone={signal_phone}&apikey={signal_apikey}&text={text}'
    return requests.get(url).text


def telegram(message: str) -> str:
    """Send a Telegram message."""

    assert telegram_username is not None

    text = quote(message)
    url = f'https://api.callmebot.com/text.php?user={telegram_username}&text={text}'
    return requests.get(url).text
