import time
from datetime import datetime
from bs4 import BeautifulSoup
import re
import os
import json


def save_files(final_html_code, html_code, history):
    time_stamp = time.time()
    file_name = datetime.fromtimestamp(
        time_stamp).strftime('%Y%m%d%H%M%S')
    path = './examples/games/{}'.format(file_name)
    os.mkdir(path)
    write_to_directory(path, html_code, 'home.html')
    write_to_directory(path, final_html_code, 'final_home.html')
    write_to_directory(path, json.dumps(history), 'history.json')


def write_to_directory(path, content, name):
    with open("{}/{}".format(path, name), "w") as output_file:
        output_file.write(content)


def parse_javascript(content):
    pattern = r'```javascript(.*?)```'
    javascript_code = re.findall(pattern, content, re.DOTALL)[0]
    return javascript_code


def parse_html(content):
    soup = BeautifulSoup(content, "html.parser")
    html = soup.find("html")
    return html.prettify()
