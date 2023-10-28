from flask import Flask, request, render_template, redirect, url_for, render_template_string
from app.main import startup_company, feed_back
from app.utils import find_project, query_projects

appz = Flask(__name__)


@appz.route('/', methods=['POST', 'GET'])
def index_create():
    if request.method == 'POST':
        data = request.get_json()

        sha = startup_company(data['ask'], project_name=data['project_name'])

        return redirect(url_for('show_update', sha_id=sha))
    elif request.method == 'GET':
        projects = query_projects()
        return render_template('index.html', projects=projects)


@appz.route('/new', methods=['GET'])
def new():
    if request.method == 'GET':
        return render_template('new.html')


@appz.route('/<sha_id>/edit', methods=['GET'])
def edit(sha_id):
    if request.method == 'GET':
        return render_template('edit.html', sha_id=sha_id)


@appz.route('/<sha_id>/play', methods=['GET'])
def play(sha_id):
    if request.method == 'GET':
        project = find_project(sha_id)
        return render_template_string(project.html)


@appz.route('/<sha_id>', methods=['POST', 'GET'])
def show_update(sha_id):
    if request.method == 'POST':
        data = request.form['feedback']
        sha = feed_back(data, sha_id)
        return redirect(url_for('update', sha_id=sha))
    elif request.method == 'GET':
        project = find_project(sha_id)
        return render_template('show.html', project=project)


if __name__ == '__main__':
    appz.run(host='0.0.0.0', debug=True)
