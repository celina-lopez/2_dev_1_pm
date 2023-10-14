import openai
import os
from dotenv import load_dotenv
# import pdb
from utils import save_files, parse_javascript, parse_html
from generative_agents import x____create_game_designer, create_project_manager, create_javascript_designer, create_html_designer

load_dotenv(dotenv_path='../.env')

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = 'gpt-3.5-turbo'

ASK = 'flappy bird'  # Use for create_project_manager

# TODO:  write history!


def startup_company(ask):
    pm_message = create_project_manager(ask)
    html_message = create_html_designer(ask, pm_message)
    html_code = parse_html(html_message)
    javascript_message = create_javascript_designer(ask, pm_message, html_code)
    javascript_code = parse_javascript(javascript_message)
    save_files(javascript_code, html_code)

# pdb.set_trace()


startup_company(ASK)
