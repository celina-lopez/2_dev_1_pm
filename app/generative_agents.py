import boto3
import openai
import os
from dotenv import load_dotenv
import requests
import uuid

load_dotenv(dotenv_path='../.env')
openai.api_key = os.getenv("OPENAI_API_KEY")
session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
)
s3 = session.resource('s3')
MODEL = 'gpt-3.5-turbo'
BUCKET = os.getenv("IMAGE_BUCKET_NAME")
PERSONAS = {
    "project_manager": {
        "system": """You are a project manager at a gaming startup company.
      Your goal is to design a simple game in javascript.
      You just met with the CEO who said they want to build this game: {}.
      You are meeting with the an Enginner.  
      You will need give an outline and description of the basic concepts and gameplay mechanics of the game in order for the Engineer to build it.
      """,
        "user": "What is the game about? Could you give me a outline and description? What are the basic concepts and gameplay mechanics?"
    },
    "game_designer": {
        "system": """
        Your goal is to design a simple game in javascript.
        You work for a gaming startup company.
        You are talking to a Project Manger who wants you to build this: {}.
        """,
        "user": "Give back only the HTML with all the code within including Javascript and CSS."
    },
    'feedback_pm': {
        'system': """
        You are a Project Manager at a gaming startup company. The CEO has asked you to build a game called {}.
        The CEO gave you this feedback: {}.
        You are talking to the Enginner.
        """,
        'user': "What is the feedback?"
    },
    'feedback_eng': {
        'system': """
        I am a Project Manager that is giving you feedback.
        Here is the HTML code for the game: {}.
        Give back only the improved HTML with all the code within including javascript and css.
        """,
    },
    'designer': {
        'system': """
        You are a designer at a gaming startup company.
        Your goal is to design the cover art for this new game: {}.
        You inputting a Dalle-3 Image Generation prompt that will generate the cover art for the game.
        ONLY GIVE THE DALLE-3 PROMPT.
        Prompt must be length 1000 or less.
        """,
        'user': "Give back the Dalle-3 prompt for the cover art for the game. ONLY GIVE THE DALLE-3 PROMPT"
    }
}


def create_persona(persona, args, user_content=None):
    messages = [
        {"role": "system",
            "content": PERSONAS[persona]['system'].format(*args)},
        {"role": "user",
            "content": user_content or PERSONAS[persona]['user']},
    ]
    response = openai.ChatCompletion.create(model=MODEL, messages=messages)
    return response.choices[0].message.content


def dalle_3_designer(pm_message):
    response = openai.Image.create(
        prompt=pm_message,
        n=1,
        size="512x512"
    )
    url = response['data'][0]['url']
    data = requests.get(url).content
    uid = str(uuid.uuid4())
    key = f'{uid}.png'
    s3.Bucket(BUCKET).put_object(Key=key, Body=data)
    return f"https://{BUCKET}.s3.amazonaws.com/{key}"
