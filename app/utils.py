from bs4 import BeautifulSoup
import re
import uuid
from app.models.base import ProjectModel


def save_project(html_code, history, project_name, image_url):
    uid = str(uuid.uuid4())
    ProjectModel(
        uid,
        title=project_name,
        logs=history,
        html=html_code,
        image=image_url
    ).save()
    return uid


def find_project(sha):
    for project in ProjectModel.query(sha):
        return project


def update_project(sha, new_html_code, logs):
    project = find_project(sha)
    project.html = new_html_code
    project.logs = logs
    project.save()
    return project


def query_projects(lastKey=None):
    project_query = ProjectModel.scan(limit=20, last_evaluated_key=lastKey)
    projects = []
    for project in project_query:
        projects.append(project)
    return projects


def parse_javascript(content):
    pattern = r'```javascript(.*?)```'
    javascript_code = re.findall(pattern, content, re.DOTALL)[0]
    return javascript_code


def parse_html(content):
    soup = BeautifulSoup(content, "html.parser")
    html = soup.find("html")
    return html.prettify()
