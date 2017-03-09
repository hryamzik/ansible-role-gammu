#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import yaml
import argparse

def main():
    parser = argparse.ArgumentParser(description='Process sms handler options')
    parser.add_argument("-i", "--interactive", help="run in interactive mode to get chat id, pass config file path. Config file should contain 'bot_key'" )
    parser.add_argument("-p", "--phone", help="phoneid" )
    args = parser.parse_args()

    configPath = None
    if args.interactive:
        configPath = args.interactive
    else:
        # configPath = "/etc/gammu.d/report-%s.yml" % os.environ['PHONE_ID'] – no such env!
        configPath = "/etc/gammu.d/report-%s.yml" % args.phone

    stream = open(configPath, "r")
    conf = yaml.load(stream)


    args = parser.parse_args()
    if args.interactive:
        from telegram.ext import Updater
        from telegram.ext import CommandHandler
        updater = Updater(token=conf['bot_key'])
        dispatcher = updater.dispatcher
        def start(bot, update):
            print ("Chatid is %d" % update.message.chat_id)
            bot.sendMessage(chat_id=update.message.chat_id, text=("Chatid is %d" % update.message.chat_id ))

        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)
        print ("Starting bot, stop with ctrl+z")
        updater.start_polling()
    else:
        numparts = int(os.environ['DECODED_PARTS'])
        text = ''
        if numparts == 0:
            text = os.environ['SMS_1_TEXT']
        else:
            for i in range(0, numparts):
                varname = 'DECODED_%d_TEXT' % i
                if varname in os.environ:
                    text = text + os.environ[varname]
    

        # Do something with the text
        chat_msg = ('%s: %s' % (os.environ['SMS_1_NUMBER'], text))

        try:
            from telegram.ext import Updater
            import logging
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            updater = Updater(token=conf['bot_key'])
            updater.bot.sendMessage(chat_id=conf['chat_id'], text=chat_msg)
        except:
            print ("Telegram send failed, using SMTP")
            import smtplib
            from email.mime.text import MIMEText

            msg = MIMEText(text)
            msg['Subject'] = "SMS from %s" % (os.environ['SMS_1_NUMBER'])
            msg['From'] = "roman.belyakovsky@gmail.com"
            msg['To'] = conf['mail_to']

            # Send the message via our own SMTP server, but don't include the
            # envelope header.
            s = smtplib.SMTP('localhost')
            s.sendmail(msg['From'], [msg['To']], msg.as_string())
            s.quit()

if __name__ == '__main__':
    main()
