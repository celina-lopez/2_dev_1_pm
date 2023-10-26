from bs4 import BeautifulSoup
import re
import uuid
from app.models.base import ProjectModel


def save_project(html_code, history, project_name):
    uid = str(uuid.uuid4())
    ProjectModel(
        uid,
        title=project_name,
        logs=history,
        html=html_code
    ).save()
    return uid


def read_history_json(sha):
    project = ProjectModel.get(sha)
    return project.logs


def parse_javascript(content):
    pattern = r'```javascript(.*?)```'
    javascript_code = re.findall(pattern, content, re.DOTALL)[0]
    return javascript_code


def parse_html(content):
    soup = BeautifulSoup(content, "html.parser")
    html = soup.find("html")
    return html.prettify()
