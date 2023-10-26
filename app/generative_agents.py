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
      You just met with the CEO who said they want to build this game: {}.
      You are meeting with the an Enginner.  
      You will need give an outline and description of the basic concepts and gameplay mechanics of the game in order for the Engineer to build it.
      """.format(ask)
        },
        {
            "role": "user",
            "content": "What is the game about? Could you give me a outline and description? What are the basic concepts and gameplay mechanics?"
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
      You work for a gaming startup company.
      You are talking to a Project Manger who wants you to build this: {}.
      """.format(ask, pm_message)
        },
        {
            "role": "user",
            "content": "Give back only the HTML with all the code within including Javascript and CSS."
        },
    ]
    response = openai.ChatCompletion.create(model=MODEL, messages=messages)
    return response.choices[0].message.content


def feed_back_pm(feedback, ask):
    messages = [
        {
            "role": "system",
            "content": """
            You are a Project Manager at a gaming startup company. The CEO has asked you to build a game called {}.
            The CEO gave you this feedback: {}.
            You are talking to the Enginner.
      """.format(ask, feedback)
        },
        {
            "role": "user",
            "content": "What is the feedback?"
        },
    ]
    response = openai.ChatCompletion.create(model=MODEL, messages=messages)
    return response.choices[0].message.content


def feed_back_eng(html_code, project_description, pm_feedback):
    messages = [
        {
            "role": "system",
            "content": """
        You need to correct the game designer's mistakes. I am a Project Manager that is giving you feedback.
        Here is the HTML code for the game: {}. Here is also the project timeline/description: {}
      Give back only the HTML with all the code within including javascript and css.
      """.format(html_code, project_description)
        },
        {
            "role": "user",
            "content": pm_feedback
        },
    ]
    response = openai.ChatCompletion.create(model=MODEL, messages=messages)
    return response.choices[0].message.content


def create_designer(ask):
    messages = [
        {
            "role": "system",
            "content": """You are a designer at a gaming startup company.
      Your goal is to design the cover art for this new game: {}.
      You inputting a Dalle-3 Image Generation prompt that will generate the cover art for the game.
    ONLY GIVE THE DALLE-3 PROMPT.
    Prompt must be length 1000 or less.
      """.format(ask)
        },
        {
            "role": "user",
            "content": "Give back the Dalle-3 prompt for the cover art for the game. ONLY GIVE THE DALLE-3 PROMPT"
        },
    ]
    response = openai.ChatCompletion.create(model=MODEL, messages=messages)
    return response.choices[0].message.content


def dalle_3_designer(pm_message):
    response = openai.Image.create(
        prompt=pm_message,
        n=1,
        size="512x512"
    )
    return response['data'][0]['url']
