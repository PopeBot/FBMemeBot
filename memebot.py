#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""TODO: Write project description"""

import sys
import logging
import ConfigParser

import FBBack


class Logr:
    """Abstraction layer for logs"""
    log_format = None
    root_logger = None
    file_handler = None
    console_handler = None

    def initiate_file_handler(self):
        """Adds file logs"""
        self.file_handler = logging.FileHandler("logs.txt")
        self.file_handler.setFormatter(self.log_format)
        self.root_logger.addHandler(self.file_handler)

    def initiate_console_handler(self):
        """Adds console logs"""
# TODO:
#       add options to reset logs on new launch
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.log_format)
        self.root_logger.addHandler(self.console_handler)

    def __init__(self, log_to_file, custom_format=""):
        """Initiates logers"""
        if custom_format is not "":
            self.log_format = logging.Formatter(custom_format)
        else:
            self.log_format = logging.Formatter("[%(asctime)s] [%(threadName)s] [%(levelname)s] : %(message)s")
        self.root_logger = logging.getLogger()
        self.root_logger.setLevel(logging.DEBUG)

        if log_to_file is True:
            self.initiate_file_handler()
        self.initiate_console_handler()

    def log(self, message):
        self.root_logger.info(message)

    def debug(self, message):
        self.root_logger.debug(message)

    def error(self, message):
        self.root_logger.error(message)


logr = Logr(True)


class Confgr:
    """Abstraction layer for configuration and credentials
        management """
    config = ConfigParser.ConfigParser()

    # Facebook
    fb_pass = ""
    fb_email = ""
    fb_chat_id = ""
    fb_admin_id = ""
    fb_bot_user = ""

    # MemeBot
    stopMSG = ""
    startMSG = ""
    updateMSG = ""

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
            self.updateMSG = self.config.get("MemeBot", "updateMSG")
        except:
            logr.error("failed to load configuration")
            sys.exit(-1)
        logr.log("succesfuly loaded configuration")


confgr = Confgr("config.ini")
