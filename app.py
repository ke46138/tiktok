from flask import Flask
import flask
import json

from databaser import Databaser


app = Flask(__name__)
db = Databaser()


@app.route('/')
def root():
    video = db.get_random_video()
    return flask.render_template(
        'index.html', 
        video=video,
        next_video=db.get_random_video([video['id']]))


@app.route('/next')
def next():
    history = flask.request.args.get('hist')

    print(history)

    if history == 'null':
        history = None
    else:
        history = history.rstrip(',')
        history = list(map(int, history.split(',')))

    return json.dumps(db.get_random_video(history))


@app.route('/get_<video_id>')
def get_video(video_id):
    return json.dumps(db.get_video(int(video_id)))


if __name__ == '__main__':
    app.run(debug=True)