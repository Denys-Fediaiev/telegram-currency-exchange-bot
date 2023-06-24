import telebot
import os
import requests
import logging
from requests.structures import CaseInsensitiveDict

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = "#"

bot = telebot.TeleBot("#")


logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm Bot That will help you to convert currencies!\n If you want to start type /exchange")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     bot.reply_to(message, message.text)

@bot.message_handler(commands=['help', 'list'])
def currency_list(message):
    bot.reply_to(message, "Here's currency codes supported by us:\n" 
    """
    EUR
    USD
    JPY
    BGN
    CZK
    DKK
    GBP
    HUF
    PLN
    RON
    SEK
    CHF
    ISK
    NOK
    HRK
    RUB
    TRY
    AUD
    BRL
    CAD
    CNY
    HKD
    IDR
    ILS
    INR
    KRW
    MXN
    MYR
    NZD
    PHP
    SGD
    THB
    ZAR """)


def currency_exchanger(currency_in: str, currency_out: str):
    url = "https://api.freecurrencyapi.com/v1/latest"
    headers = CaseInsensitiveDict()
    headers["apikey"] = API_KEY
    params = {"base_currency": currency_in, "currencies": currency_out}
    response = requests.get(url, headers=headers, params=params)
    return response.json()


@bot.message_handler(commands=['exchange'])
def currency_in_handler(message):
    text = "What's currency do you want to change?\nChoose one: *USD*, *EUR*, *CAD*, *JPY*, etc. \n ***Please use only currency CODES***\n/help"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, currency_out_handler)


def currency_out_handler(message):
    currency_in = message.text
    text = "what currency do you want to convert to?"
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, amount_handler, currency_in.upper())


def amount_handler(message, currency_in):
    currency_out = message.text
    text = f"what amount of {currency_in} do you want to convert to {currency_out}?"
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, currency_fetch, currency_in.upper(), currency_out.upper())


def currency_fetch(message, currency_in, currency_out):
    amount = float(message.text)
    exchange_c = currency_exchanger(currency_in, currency_out)
    print(exchange_c)
    logging.info(f"json format: {exchange_c}")
    logging.info(f"currency code IN: {currency_in}")
    logging.info(f"currency code OUT: {currency_out}")
    logging.info(f"amount: {amount}")
    try:
        data = exchange_c['data']
        logging.info(f"fetching successful with data result:{data}")
    except:
        logging.error(f"Error: {data}", exc_info=True)
    result = data[currency_out] * amount
    exchange_message = f'Current {currency_in} to {currency_out} rate is  {data[currency_out]}\n*your currency:* {currency_in} {amount}\n*you get:* {currency_out} {result}'
    bot.send_message(message.chat.id, "Here's your info!")
    bot.send_message(message.chat.id, exchange_message, parse_mode="Markdown")





bot.infinity_polling()

