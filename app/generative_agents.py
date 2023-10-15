import openai
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = 'gpt-3.5-turbo'


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
    return response.choices[0].message.content


def create_game_reviewer(html_code):
    messages = [
        {
            "role": "system",
            "content": "Your goal is to review a game that was built in html and javascript. You will need to provide the corrected HTML code back."
        },
        {
            "role": "user",
            "content": """ 
            Could you review the game and rewrite the code in a way that is more efficient? If you can't, return the HTML code.
            Here is the code: {}.
            """.format(html_code)
        },
    ]
    response = openai.ChatCompletion.create(model=MODEL, messages=messages)
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
    return response.choices[0].message.content
