import json
import time
from datetime import datetime
from bs4 import BeautifulSoup
import re


def save_files(messages):
    time_stamp = time.time()
    file_name = datetime.fromtimestamp(
        time_stamp).strftime('sample_%Y-%m-%d%H:%M:%S')
    write_messages(file_name, messages)
    # write_html(file_name, messages[-1]["content"])
    write_text(file_name, messages[-1]["content"])


def write_messages(file_name, messages):
    with open("../examples/jsons/{}.json".format(file_name), 'w') as outfile:
        json.dump(messages, outfile)


def write_text(file_name, content):
    with open("../examples/texts/{}.txt".format(file_name), "w") as output_file:
        output_file.write(content)


def write_html(file_name, content):
    soup = BeautifulSoup(content, "html.parser")
    html = soup.find("html")
    with open("../examples/htmls/{}.html".format(file_name), "w") as output_file:
        output_file.write(html.prettify())


def write_javascript(file_name, content):
    pattern = r'```javascript(.*?)```'
    javascript_code = re.findall(pattern, content, re.DOTALL)[0]
    with open("../examples/javascripts/{}.js".format(file_name), "w") as js_file:
        js_file.write(javascript_code)
