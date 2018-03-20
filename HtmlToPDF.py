import pdfkit
import os
import re


options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ],
    'cookie': [
        ('cookie-name1', 'cookie-value1'),
        ('cookie-name2', 'cookie-value2'),
    ],
    'outline-depth': 10,
}
htmls = []
for root, dirs, files in os.walk("./"):
    for file in files:
        obj = re.search(r".*html", file)
        if obj is not None:
            htmls.append(obj.group())
pdfkit.from_url(htmls, 'out_0.pdf', options=options)
