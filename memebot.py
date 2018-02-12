#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""TODO: Write project description"""

import os
import sys
import random
import configparser

from fbchat import log
from fbchat.models import *
from fbchat import Client as FBClient


class Confgr:
    """Abstraction layer for configuration and credentials
        management """
    config = configparser.ConfigParser()

    # Facebook
    fb_pass = ""
    fb_email = ""
    fb_chat_id = ""
    fb_admin_id = ""
    fb_bot_user = ""

    # MemeBot
    stopMSG = ""
    startMSG = ""
    memesDIR = ""

    def __init__(self, config_path):
        """Reads configuration from given file"""
        try:
            self.config.read(config_path)

            self.fb_pass = self.config.get("Facebook", "Pass")
            self.fb_email = self.config.get("Facebook", "Email")
            self.fb_chat_id = self.config.get("Facebook", "ChatID")
            self.fb_admin_id = self.config.get("Facebook", "AdminID")
            self.fb_bot_user = self.config.get("Facebook", "BotName")

            self.stopMSG = self.config.get("MemeBot", "stopMSG")
            self.startMSG = self.config.get("MemeBot", "startMSG")
            self.memesDIR = self.config.get("MemeBot", "memesDIR")
        except:
            log.info("Failed to load configuration")
            sys.exit(-1)
        log.info("Succesfuly loaded configuration")


confgr = Confgr("config.ini")


class MemeBot(FBClient):
    """Class description"""

    def exit(self):
        if confgr.stopMSG is not None:
            with open(confgr.stopMSG, "r") as stopFile:
                msg = stopFile.read()
                self.send(Message(msg), confgr.fb_chat_id, thread_type=ThreadType.GROUP)

        self.logout()
        log.info("Powering off...")
        sys.exit(0)

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        if author_id == self.uid:
            log.info("Skipping own messages")
            return

        if author_id == confgr.fb_admin_id:
            if message_object.text == "/down":
                self.exit()

        if message_object.text == "@" + str(confgr.fb_bot_user):
            self.sendMeme(thread_id, thread_type)

    def sendMeme(self, thread_id, thread_type=ThreadType.GROUP):
        memePath = str(confgr.memesDIR + random.choice(os.listdir(confgr.memesDIR)))
        self.sendLocalImage(memePath, thread_id=thread_id, thread_type=thread_type)
        log.info("Sending %s meme", memePath)


fb_bot = MemeBot(confgr.fb_email, confgr.fb_pass)

if confgr.startMSG is not None:
    with open(confgr.startMSG, "r") as startFile:
        msg = startFile.read()
        fb_bot.send(Message(msg), thread_id=confgr.fb_chat_id, thread_type=ThreadType.GROUP)

fb_bot.listen()
