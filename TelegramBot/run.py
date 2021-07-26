#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

import logging
import requests
import jsonpickle

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CAR, LICENSE_PLATE, PHOTO, DESCRIPTION = range(4)


def start(bot, update):
    reply_keyboard = [['Yes', 'No']]

    update.message.reply_text(
        'Hi! I\'m from the future and i\'m in charge of entrance approvals. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Do you want to enter with a car?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CAR


def licence_plate(bot, update, user_data):
    user_data['plate'] = update.message.text
    update.message.reply_text(
        'Thank You. Now, please send me a photo of your ID',
        reply_markup=ReplyKeyboardRemove())
    return PHOTO


def car(bot, update, user_data):
    user = update.message.from_user
    user_data['car'] = update.message.text
    logger.info("%s: enters with a car? %s", user.first_name, update.message.text)
    if update.message.text == 'Yes':
        update.message.reply_text('I see! Please send me your license plate number.',
                                  reply_markup=ReplyKeyboardRemove())
        return LICENSE_PLATE
    else:
        update.message.reply_text('I see! Please send me a photo of your ID',
                                  reply_markup=ReplyKeyboardRemove())
        return PHOTO


def photo(bot, update, user_data):
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    user_data['photo'] = photo_file
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Gorgeous! What is the reason for entrance?')

    return DESCRIPTION


def description(bot, update, user_data):
    user = update.message.from_user
    user_data['description'] = update.message.text
    user_data['user'] = user
    user_data['chat_id'] = update.message.chat_id
    logger.info("Description of %s: %s", user.first_name, update.message.text)
    process_data(user_data)

    update.message.reply_text('Thank you! Your entrance request was processed and sent for appproval')
    return ConversationHandler.END


def process_data(user_data):
    body = {
        'photo': user_data['photo'].download_as_bytearray(),
        'user': user_data['user'],
        'description': user_data['description'],
        'plate': user_data['plate'] if 'plate' in user_data else None,
        'chat_id': user_data['chat_id']
    }

    url = 'http://10.104.236.26:8080/api/AddEntryPermit'
    requests.post(url, data=jsonpickle.encode(body))
    return body


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("951740858:AAHDXXwE0dYA3UTXQnetnPq5D2FWlWqKqw4")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CAR: [RegexHandler('^(Yes|No)$', car, pass_user_data=True)],
            LICENSE_PLATE: [RegexHandler('^[0-9]{7,8}$', licence_plate, pass_user_data=True)],
            PHOTO: [MessageHandler(Filters.photo, photo, pass_user_data=True)],
            DESCRIPTION: [MessageHandler(Filters.text, description, pass_user_data=True)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    print("Start Polling")
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()