import openai
import os
from dotenv import load_dotenv
import pdb
from utils import save_files
from generative_agents import x____create_game_designer, create_project_manager, create_javascript_designer

load_dotenv(dotenv_path='../.env')

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = 'gpt-3.5-turbo'

ASK = 'flappy bird'  # Use for create_project_manager


def startup_company(ask):
    messages = create_javascript_designer(ask, create_project_manager(ask))
    save_files(messages)

# pdb.set_trace()


startup_company(ASK)
