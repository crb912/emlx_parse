from collections import namedtuple
import email

from emlx_parse import emlx_utils


Header = namedtuple('Header',
                    'msg_id subject from_ to cc bcc date_utc received reply_to')
Body = namedtuple(
    'Body',
    'charset maintype subtype text_plain text_html filename ' +
    'image attachment content_id')
Received = namedtuple('Received', 'date_utc last_view_date_utc')


class Email:
    def __init__(self, src_data, plist_data, decode: bool):
        self._src_email = src_data
        self._src_plist = plist_data
        self._decode = decode

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
        return email_header

    def get_body(self):
        for part in self._src_email.walk():
            text_plain = None
            text_html = None
            image = None
            attachment = {}
            payload = part.get_payload(decode=self._decode)
            charset = part.get_content_charset()
            content_id = part.get('content-id')
            if isinstance(content_id, str):
                content_id = content_id.replace('<', '')
                content_id = content_id.replace('>', '')
            disposition = part.get_content_disposition()
            content_type = self.decode_header(part.get_content_type())
            maintype = content_type.split('/')[0]
            subtype = content_type.split('/')[1]
            file_name = self.decode_header(part.get_filename())
            if 'text' == maintype and 'plain' == subtype and charset:
                text_plain = str(payload.decode(charset))
            if 'text' == maintype and 'html' == subtype and charset:
                text_html = str(payload.decode(charset))
            if 'inline' == disposition:
                image = payload
            if 'attachment' == disposition and self._decode is True:
                attachment = payload
            item = Body(
                charset=charset, maintype=maintype, subtype=subtype,
                text_plain=text_plain, text_html=text_html, filename=file_name,
                image=image, attachment=attachment, content_id=content_id
            )
            yield item

    def get_received(self):
        date_utc = emlx_utils.convert_time_from_plist(
            self._src_plist.get('date-received'))
        last_view_date_utc = emlx_utils.convert_time_from_plist(
            self._src_plist.get('date-last-viewed'))
        if not date_utc:
            date_utc = emlx_utils.convert_time(self._src_email.get('Received'))
        receive = Received(
            date_utc=date_utc,
            last_view_date_utc=last_view_date_utc,
        )
        return receive

    def get_text(self):
        pass

    @staticmethod
    def decode_header(data: str):
        if not isinstance(data, str):
            return
        return str(email.header.make_header(email.header.decode_header(data)))
