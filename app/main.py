import openai
import os
from dotenv import load_dotenv
import json
from app.utils import save_project, parse_html
from app.generative_agents import create_persona, dalle_3_designer

load_dotenv(dotenv_path='../.env')

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = 'gpt-3.5-turbo'


def startup_company(ask, project_name=''):
    pm_message = create_persona('project_manager', ask)
    html_message = create_persona('game_designer', (ask, pm_message))
    html = parse_html(html_message)
    designer_message = create_persona('designer', ask)
    image_url = dalle_3_designer(designer_message)
    history = [{
        'ask': ask,
        "pm_message": pm_message,
        "html_message": html_message,
    }]
    uuid = save_project(html, history, project_name, image_url)
    return uuid


def feed_back(feedback, sha):
    with open('./examples/games/{}/history.json'.format(sha)) as json_file:
        history = json.load(json_file)
    ask = history[-1]['ask']
    with open('./examples/games/{}/home.html'.format(sha), 'r') as outfile:
        html_code = outfile.read()
    feedback_message = create_persona('feedback_pm', "\n".join(feedback), ask)
    feedback_html_code = create_persona(
        'feedback_eng', (html_code, history[0]['pm_message']), user_content=feedback_message)
    new_html_code = parse_html(feedback_html_code)
    new_history = {
        'ask': ",".join(feedback_message),
        "pm_message": feedback_message,
        "html_message": feedback_html_code,
    }
    history.append(new_history)
    sha = save_project(new_html_code, history)  # TODO: update project
    return sha
