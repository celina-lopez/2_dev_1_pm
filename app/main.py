import openai
import os
from dotenv import load_dotenv
import pdb
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup

load_dotenv(dotenv_path='../.env')

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = 'gpt-3.5-turbo'

ASK = 'flappy bird' # Use for create_project_manager

def create_project_manager(ask):
  messages = [
    {
      "role": "system",
      "content": """You are a project manager at a gaming startup company.
      Your goal is to design a simple game in javascript.
      You are meeting with the CEO to discuss the company's new product launch where they will ask you to build a specific game.
      You will then need to outline the basic concepts and gameplay mechanics of the game.
      """
    },
    {
      "role": "user",
      "content": "I want to build {}".format(ask)
    },
  ]
  response = openai.ChatCompletion.create(model=MODEL, messages=messages)
  # messages.append({
  #   "role": "assistant",
  #   "content": response.choices[0].message.content,
  # })
  return response.choices[0].message.content

def create_game_designer(ask, pm_message):
  messages = [
    {
      "role": "system",
      "content": """
      Your goal is to design a simple game in javascript.
      Give back only the HTML with all the code within including javascript and css.
      """
    },
    {
      "role": "user",
      "content": "I will need you to build {}. Here is how it should work: {}.".format(ask, pm_message)
    },
  ]
  response = openai.ChatCompletion.create(model=MODEL, messages=messages)
  messages.append({
    "role": "assistant",
    "content": response.choices[0].message.content,
  })
  return messages


def startup_company(ask):
  messages = create_game_designer(ask, create_project_manager(ask))
  save_files(messages)



def save_files(messages):
  time_stamp = time.time()
  file_name = datetime.fromtimestamp(time_stamp).strftime('sample_%Y-%m-%d%H:%M:%S')
  write_messages(file_name, messages)
  write_html(file_name, messages[-1]["content"])


def write_messages(file_name, messages):
  with open("../examples/jsons/{}.json".format(file_name), 'w') as outfile:
    json.dump(messages, outfile)

def write_html(file_name, content):
  soup = BeautifulSoup(content, "html.parser")
  html = soup.find("html")
  with open("../examples/htmls/{}.html".format(file_name), "w") as output_file:
    output_file.write(html.prettify())

# pdb.set_trace()

# startup_company(ASK)
  

