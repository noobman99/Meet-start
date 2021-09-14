
import telebot

from classeditor import adlec_auto, reg_url
from classstarter import start_manual
from File import File

import os


API_KEY = ""
USER = (,)

bot = telebot.TeleBot(API_KEY)


def is_adder(message):
    if reg_url.search(message.text):
        return True
    else:
        return False


def by_user(message):
    if message.from_user.id in USER:
        return True
    else:
        return False


@bot.message_handler(commands=["add"], func=by_user)
def add_meet(message):
    if msg := message.reply_to_message:
        if is_adder(msg):
            meets = adlec_auto(msg.text)
    else:
        if is_adder(message):
            meets = adlec_auto(message.text)
    if meets:
        ret_text = "Lectures added at\n" + "\n".join(i["from"] for i in meets)
    else:
        ret_text = "Dont break the bot mate"
    bot.reply_to(message, ret_text)


@bot.message_handler(commands=["remove", "rem"], func=by_user)
def rem_meet(message):
    exception_text = "Reply to a meeting. To get list of meetings use '/meets'"
    file = File("stor.txt")
    if message.reply_to_message:
        if url := reg_url.search(message.reply_to_message.text):
            file.del_rec(url.group(0), atr="url")
            bot.reply_to(message.reply_to_message, "Deleted this meeting from TT")
        else:
            bot.reply_to(message, exception_text)
    else:
        bot.reply_to(message, exception_text)


@bot.message_handler(commands=["startnow", "sn"], func=by_user)
def inst_start(message):
    if start_manual():
        bot.send_message(message.chat.id, "Started the meeting")
    else:
        bot.send_message(message.chat.id, "No meeting at the moment")


@bot.message_handler(commands=["meets"], func=by_user)
def meetings_lister(message):
    file = File("stor.txt")
    for i in file.val:
        ret_text = "\n".join([f"{key} : {i[key]}" for key in file.keys])
        bot.send_message(message.chat.id, ret_text)


@bot.message_handler(commands=["getid"])
def give_id(message):
    bot.send_message(message.chat.id, f"hello {message.from_user.first_name}\nyour id is: {message.from_user.id}")


print("bot starting")
bot.polling()
