"""
Class to parse email stored with Apple proprietary emlx format
Reference: https://gist.github.com/karlcow/5276813
MIT License
"""

import email
import plistlib

from .emlx_email import Email


class Emlx:
    """An apple proprietary emlx message"""

    def __init__(self, file_path):
        self.file_path = file_path
        self._email_data = None
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
            # parsing the rest of the message aka the plist structure
            msg_plist = plistlib.loads(f.read())
            self._email_data = Email(msg_data, msg_plist)

    @property
    def header(self):
        return self._email_data.get_header()

    @property
    def body(self):
        return self._email_data.get_body()
