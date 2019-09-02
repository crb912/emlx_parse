import emlx_parse

sample_file_path = r'./sample/1.emlx'
my_eml = emlx_parse.Emlx(sample_file_path, decode=True)

# Header
print(my_eml.header.subject)
print(my_eml.header.from_)
print(my_eml.header.to)
print(my_eml.header.received.date_utc)
print(my_eml.header.cc)
print(my_eml.header.bcc)

# Body
for part in my_eml.body:
    if part.text_plain:
        print('# TEXT #', part.text_plain)
    if part.text_html:
        print('# HTML #', part.text_html)
    # save image
    if part.image:
        print('my image')
        with open(part.filename, 'wb') as fh:
            fh.write(part.image)
    # save other attachment
    if part.attachment:
        with open(part.filename, 'wb') as fh:
            fh.write(part.attachment)