from flask import Flask, request, send_from_directory, render_template, redirect, url_for
from app.main import startup_company, feed_back
import os

appz = Flask(__name__)


@appz.route('/', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        ask = request.get_json()['ask']
        sha = startup_company(ask)

        return redirect(url_for('update', sha_id=sha))
    elif request.method == 'GET':
        available_shas = os.listdir('examples/games')
        return render_template('list.html', shas=available_shas)


@appz.route('/new', methods=['GET'])
def create():
    if request.method == 'GET':
        return render_template('home.html')


@appz.route('/<sha_id>', methods=['PUT', 'GET'])
def update(sha_id):
    if request.method == 'POST':
        data = request.form
        sha = feed_back(data['feedback'], sha_id)
        return {'sha': sha}
    elif request.method == 'GET':
        return send_from_directory('examples/games/{}'.format(sha_id), 'home.html')


if __name__ == '__main__':
    appz.run(host='0.0.0.0', debug=True)
