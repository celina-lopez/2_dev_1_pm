import openai
import os
from dotenv import load_dotenv
import json
import pdb
from app.utils import save_project, parse_html
from app.generative_agents import create_game_designer, create_project_manager, feed_back_pm, feed_back_eng, create_designer, dalle_3_designer

load_dotenv(dotenv_path='../.env')

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = 'gpt-3.5-turbo'

ASK = 'flappy bird'  # Use for create_project_manager

# TODO:  write history!


def startup_company(ask, project_name=''):
    pm_message = create_project_manager(ask)
    html_message = create_game_designer(ask, pm_message)
    html_code = parse_html(html_message)
    designer_message = create_designer(ask)
    image_url = dalle_3_designer(designer_message)
    history = [{
        'ask': ask,
        "pm_message": pm_message,
        "html_message": html_message,
        'image_url': image_url
    }]
    sha = save_project(html_code, history, project_name)
    return sha


def sample_function(sha):
    user_input = input("Enter a list of values separated by commas: ")
    user_list = user_input.split(',')
    user_list = [item.strip() for item in user_list]
    feed_back(user_list, sha)


def feed_back(feedback, sha):
    with open('./examples/games/{}/history.json'.format(sha)) as json_file:
        history = json.load(json_file)
    ask = history[-1]['ask']
    with open('./examples/games/{}/home.html'.format(sha), 'r') as outfile:
        html_code = outfile.read()
    feedback_message = feed_back_pm(
        "\n".join(feedback), ask)  # feed back is a list
    feedback_html_code = feed_back_eng(
        feedback_message, history[0]['pm_message'], html_code)
    new_html_code = parse_html(feedback_html_code)
    new_history = {
        'ask': ",".join(feedback_message),
        "pm_message": feedback_message,
        "html_message": feedback_html_code,
        "prevous_sha": sha,
    }
    history.append(new_history)
    sha = save_project(new_html_code, history)
    return sha
# pdb.set_trace()

# app.main.sample_function("20231014185300")
# the game is too fast could we slow it down, the game over should not be a pop up but displayed over the canvas, make the background of the the game light blue

# startup_company(ASK)
