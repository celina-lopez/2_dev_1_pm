import openai
import os
from dotenv import load_dotenv
from app.utils import save_project, parse_html, update_project, find_project
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
        'designer_message': designer_message,
        'image_url': image_url
    }]
    uuid = save_project(html, history, project_name, image_url)
    return uuid


def feed_back(feedback, sha):
    project = find_project(sha)
    logs = project.logs
    html_code = project.html
    feedback_message = create_persona('feedback_pm', feedback, logs[0]['ask'])
    feedback_html_code = create_persona(
        'feedback_eng', (html_code, logs[0]['pm_message']), user_content=feedback_message)
    new_html_code = parse_html(feedback_html_code)
    new_history = {
        'ask': feedback,
        "pm_message": feedback_message,
        "html_message": feedback_html_code,
    }
    logs.append(new_history)
    update_project(sha, new_html_code, logs)
