from collections import namedtuple
import email

from . import emlx_utils


Header = namedtuple('Header',
                    'msg_id subject from_ to cc bcc date_utc received reply_to')
Body = namedtuple(
    'Body',
    'charset maintype subtype text_plain text_html filename image attachment')
Received = namedtuple('Received', 'date_utc')


class Email:
    def __init__(self, src_data, plist_data):
        self._src_email = src_data
        self._src_plist = plist_data

    def get_header(self):
        date_utc = emlx_utils.convert_time(self._src_email.get('Date'))
        received = self.get_received()
        email_header = Header(
            msg_id=self._src_email.get('Message-Id'),
            subject=self.decode_header(self._src_email.get('Subject')),
            from_=self.decode_header(self._src_email.get('From')),
            to=self.decode_header(self._src_email.get('To')),
            cc=self.decode_header(self._src_email.get('Cc')),
            bcc=self.decode_header(self._src_email.get('Bcc')),
            date_utc=date_utc,
            received=received,
            reply_to=None
        )
        self.get_body()
        return email_header

    def get_body(self):
        if self._src_email.is_multipart():
            return self.get_body_multipart()
        else:
            return self.get_body_direct()

    def get_body_direct(self):
        text_plain = None
        text_html = None
        image = None
        payload = self._src_email.get_payload(decode=True)
        charset = self._src_email.get_content_charset()
        maintype = self._src_email.get_content_maintype()
        subtype = self._src_email.get_content_subtype()
        file_name = self._src_email.get_filename()
        if 'text' == maintype and 'plain' == subtype:
            text_plain = payload.decode(charset)
        if 'text' == maintype and 'html' == subtype:
            text_html = payload.decode(charset)
        if 'image' == maintype:
            image = payload
        item = Body(
            charset=charset, maintype=maintype, subtype=subtype,
            text_plain=text_plain, text_html=text_html,
            filename=file_name, image=image, attachment=None
        )
        body = [item]
        return body

    def get_body_multipart(self):
        body = []
        for part in self._src_email.walk():
            text_plain = None
            text_html = None
            image = None
            payload = part.get_payload(decode=True)
            charset = part.get_content_charset()
            maintype = part.get_content_maintype()
            subtype = part.get_content_subtype()
            file_name = part.get_filename()
            # TODO: TypeError: decode() argument 1 must be str, not None
            # if 'text' == maintype and 'plain' == subtype:
            #     text_plain = payload.decode(charset)
            # if 'text' == maintype and 'html' == subtype:
            #     text_html = payload.decode(charset)
            # if 'image' == maintype:
            #     image = payload
            item = Body(
                charset=charset, maintype=maintype, subtype=subtype,
                text_plain=text_plain, text_html=text_html, filename=file_name,
                image=image, attachment=None
            )
            # print('&&&')
            # print(item)
            body.append(item)
        return body

    def get_received(self):
        date_utc = emlx_utils.convert_time(self._src_email.get('Received'))
        if not date_utc:
            # TODO:从plist中取出时间
            date_utc = None
        receive = Received(
            date_utc=date_utc
        )
        return receive

    def get_text(self):
        pass

    @staticmethod
    def decode_header(data: str):
        if not isinstance(data, str):
            return
        return str(email.header.make_header(email.header.decode_header(data)))
