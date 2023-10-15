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


def feed_back_pm(feedback, ask):
    messages = [
        {
            "role": "system",
            "content": """
   You are a project manager at a gaming startup company. The CEO has asked you to build a game called {}.
   The game is broken and you need to give feedback to the game designer.

      """.format(ask)
        },
        {
            "role": "user",
            "content": "I have a list of bugs that need to be fixed. Could you go back to your game engineer and say what needs to be done? Here are the bugs: {}".format(feedback)
        },
    ]
    response = openai.ChatCompletion.create(model=MODEL, messages=messages)
    return response.choices[0].message.content


def feed_back_eng(html_code, pm_feedback):
    messages = [
        {
            "role": "system",
            "content": """
        You need to correct the game designer's mistakes. The Project Manager will give you feedback.
        Here is the game: {}.
      Give back only the HTML with all the code within including javascript and css.
      """.format(html_code)
        },
        {
            "role": "user",
            "content": "Here is some feedback on the current game: {}. Rewrite the HTML code".format(pm_feedback)
        },
    ]
    response = openai.ChatCompletion.create(model=MODEL, messages=messages)
    return response.choices[0].message.content
# pdb.set_trace()
