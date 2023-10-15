import openai
import os
from dotenv import load_dotenv
# import pdb
from utils import save_files, parse_html
from generative_agents import create_game_designer, create_project_manager, create_game_reviewer

load_dotenv(dotenv_path='../.env')

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = 'gpt-3.5-turbo'

ASK = 'flappy bird'  # Use for create_project_manager

# TODO:  write history!


def startup_company(ask):
    pm_message = create_project_manager(ask)
    html_message = create_game_designer(ask, pm_message)
    html_code = parse_html(html_message)
    game_review_message = create_game_reviewer(html_code)
    final_html_code = parse_html(game_review_message)
    history = {
        'ask': ask,
        "pm_message": pm_message,
        "html_message": html_message,
        "game_review_message": game_review_message
    }
    save_files(final_html_code, html_code, history)

# pdb.set_trace()


startup_company(ASK)
