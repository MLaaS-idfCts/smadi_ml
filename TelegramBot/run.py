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

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, \
    ConversationHandler, CallbackQueryHandler

import logging
import requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSE, PERSONAL_NUMBER, PHONE_NUMBER, IS_COMMANDER, COMMANDER_PERSONAL_NUMBER, \
COMMANDER_PHONE_NUMBER, PHOTO, MAC_BLUETOOTH, BLUETOOTH_DEVICE_NAME = range(9)


def start(bot, update):
    reply_keyboard = [['Register', 'Delete']]

    update.message.reply_text(
        'Hi! Welcome to Smadi-ML :)\n'
        'Pleace choose an option: Register or Update',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CHOOSE


def choose(bot, update, user_data):
    user = update.message.from_user
    logger.info(f'choose: {user.first_name}: {update.message.text}')

    if update.message.text == 'Register':
        update.message.reply_text('OK! Let\'s start the registration process,\n'
                                  'Please fill in your personal number',
                                  reply_markup=ReplyKeyboardRemove())
        return PERSONAL_NUMBER
    else:
        # TODO: fill
        update.message.reply_text('Bye! I hope we can talk again some day.',
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END
        # return Delete


def personal_number(bot, update, user_data):
    user = update.message.from_user
    logger.info(f'personal_number: {user.first_name}: {update.message.text}')

    user_data['personal_number'] = update.message.text
    update.message.reply_text(
        'Thank You. Now, please click to send your phone number',
        reply_markup=KeyboardButton('Click to send the phone number', request_contact=True))

    return PHONE_NUMBER


def phone_number(bot, update, user_data):
    contact = update.effective_message.contact
    user_data['phone_number'] = contact.phone_number

    user = update.message.from_user
    logger.info(f'phone_number: {user.first_name}: {contact.phone_number}')

    reply_keyboard = [['Yes', 'No']]

    update.message.reply_text(
        'Thank You. Do you want to enter your commander\'s details?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return IS_COMMANDER


def is_commander(bot, update, user_data):
    user = update.message.from_user
    logger.info(f'is_commander: {user.first_name}: {update.message.text}')

    if update.message.text == 'Yes':
        update.message.reply_text('Please fill in your commander\'s personal number',
                                  reply_markup=ReplyKeyboardRemove())
        return COMMANDER_PERSONAL_NUMBER
    else:
        update.message.reply_text('I see! Please send me a photo of you\n'
                                  'Please make sure that the photo is in high quality!',
                                  reply_markup=ReplyKeyboardRemove())
        return PHOTO


def commander_personal_number(bot, update, user_data):
    user = update.message.from_user
    logger.info(f'commander_personal_number: {user.first_name}: {update.message.text}')

    user_data['commander_personal_number'] = update.message.text

    update.message.reply_text('Please fill in your commander\'s phone number',
                              reply_markup=ReplyKeyboardRemove())

    return COMMANDER_PHONE_NUMBER


def commander_phone_number(bot, update, user_data):
    user = update.message.from_user
    logger.info(f'commander_phone_number: {user.first_name}: {update.message.text}')

    user_data['commander_phone_number'] = update.message.text

    reply_keyboard = [['Yes', 'No']]

    update.message.reply_text('I see! Please send me a photo of you\n'
                              'Please make sure that the photo is in high quality!',
                              reply_markup=ReplyKeyboardRemove())

    return PHOTO


def photo(bot, update, user_data):
    user = update.message.from_user
    logger.info(f'photo: {user.first_name} uploaded a photo')

    photo_file = bot.get_file(update.message.photo[-1].file_id)
    user_data['photo'] = photo_file.download_as_bytearray()

    update.message.reply_text('Gorgeous! Please enter your MAC Bluetooth',
                              reply_markup=ReplyKeyboardRemove())

    return MAC_BLUETOOTH


def mac_bluetooth(bot, update, user_data):
    user = update.message.from_user
    logger.info(f'mac_bluetooth: {user.first_name}: {update.message.text}')

    user_data['mac_bluetooth'] = update.message.text
    update.message.reply_text('Please enter your Bluetooth device name',
                              reply_markup=ReplyKeyboardRemove())

    return BLUETOOTH_DEVICE_NAME


def bluetooth_device_name(bot, update, user_data):
    user = update.message.from_user
    logger.info(f'bluetooth_device_name: {user.first_name}: {update.message.text}')

    user_data['device_name'] = update.message.text
    update.message.reply_text('Please enter your Bluetooth device name')

    process_data(user_data)

    update.message.reply_text('Thank you! Your registration request was processed')

    return ConversationHandler.END



def process_data(user_data):
    'register_user/<str:personal_number>/<str:commander_id>/<str:phone_number>/<str:mac_bluetooth>/<str:device_name>/'
    user_data['commander_personal_number'] = user_data.get('commander_personal_number', None)
    user_data['commander_phone_number'] = user_data.get('commander_phone_number', None)

    url = 'http://51.137.47.10:8080/api/register_user'
    res = requests.post(url, data=user_data)

    logger.info(f'status_code: {res.status_code}')


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
    updater = Updater("951740858:ABGDXXwE0dYA3UTXQnetnPq5D2FWlWqKqw4")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],


        states={
            CHOOSE: [RegexHandler('^(Register|Delete)$', choose, pass_user_data=True)],
            PERSONAL_NUMBER: [RegexHandler('^[0-9]{7}$', personal_number, pass_user_data=True)],
            PHONE_NUMBER: [MessageHandler(Filters.contact, phone_number, pass_user_data=True)],
            IS_COMMANDER: [RegexHandler('^(Yes|No)$', is_commander, pass_user_data=True)],
            COMMANDER_PERSONAL_NUMBER: [RegexHandler('^[0-9]{7}$', commander_personal_number, pass_user_data=True)],
            COMMANDER_PHONE_NUMBER: [RegexHandler('^[0-9]{10}$', commander_phone_number, pass_user_data=True)],
            PHOTO: [MessageHandler(Filters.photo, photo, pass_user_data=True)],
            MAC_BLUETOOTH: [MessageHandler(Filters.text, mac_bluetooth, pass_user_data=True)],
            BLUETOOTH_DEVICE_NAME: [MessageHandler(Filters.text, bluetooth_device_name, pass_user_data=True)],
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
