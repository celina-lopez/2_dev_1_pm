from flask import Flask, request, send_from_directory
from app.main import startup_company, feed_back

appz = Flask(__name__)


@appz.route('/', methods=['POST'])
def create():
    if request.method == 'POST':
        ask = request.get_json()['ask']
        sha = startup_company(ask)

        return {'sha': sha}


@appz.route('/<sha_id>', methods=['PUT', 'GET'])
def update(sha_id):
    if request.method == 'POST':
        data = request.form
        sha = feed_back(data['feedback'], sha_id)
        return {'sha': sha}
    elif request.method == 'GET':
        return send_from_directory('examples/games/{}'.format(sha_id), 'home.html')


if __name__ == '__main__':
    appz.run(debug=True)
