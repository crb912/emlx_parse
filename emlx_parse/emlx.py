"""
Class to parse email stored with Apple proprietary emlx format
Created by Karl Dubost on 2013-03-30
Inspired by Rui Carmo — https://the.taoofmac.com/space/blog/2008/03/03/2211
MIT License
"""

import email

import plistlib

from .emlx_email import Email


class Emlx:
    """An apple proprietary emlx message"""

    def __init__(self, file_path, decode=False):
        """ Parse emlx file.

        :param file_path: emlx file path
        :param decode: True for decode image and attachments, False for not
        """
        self.file_path = file_path
        self._decode = decode
        self._email_data = None
        self.header = None
        self.body = None
        self.parse()

    def parse(self):
        """
        return the data structure for the current emlx file
        :return: the plist structure as a dict data structure
        """
        with open(self.file_path, "rb") as f:
            byte_count = int(f.readline().strip())
            # extract the message itself.
            msg_data = email.message_from_bytes(f.read(byte_count))
            # parsing the rest of the message aka the plist structure.
            # PLIST FORMAT: {'date-last-viewed': 1565157221,
            #                'date-received': 1565157221,
            #                'flags': 8623686721}
            msg_plist = plistlib.loads(f.read())
            self._email_data = Email(msg_data, msg_plist, self._decode)
        self.header = self._email_data.get_header()
        self.body = self._email_data.get_body()
