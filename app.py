from flask import Flask, render_template, request, redirect, url_for, flash
import flask
import json
from werkzeug.utils import secure_filename
import os

from databaser import Databaser


app = Flask(__name__)
db = Databaser()

app.config['SECRET_KEY'] = 'pass'  # Для flash сообщений
app.config['UPLOAD_FOLDER'] = 'static/videos'
app.config['ALLOWED_EXTENSIONS'] = {'mp4'}
app.config['PASSWORD'] = 'pass'  # Задайте ваш пароль

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Главная страница с формой для загрузки видео
@app.route('/upload', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        # Проверка пароля
        password = request.form.get('password')
        if password != app.config['PASSWORD']:
            flash('Неверный пароль!', 'danger')
            return redirect(request.url)

        # Проверка на наличие файла
        if 'file' not in request.files:
            flash('Нет файла для загрузки!', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('Нет выбранного файла!', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = f"{db.get_last_video_id() + 1}.mp4"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Получаем дополнительные данные
            author = request.form.get('author')
            description = request.form.get('description')
            db.add_video(description, author, db.get_last_video_id() + 1)
            
            flash(f'Видео "{filename}" успешно загружено!', 'success')
            return redirect(url_for('upload_video'))
        else:
            flash('Недопустимый формат видео!', 'danger')
            return redirect(request.url)

    return render_template('upload.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(port=443, host="0.0.0.0", ssl_context=('fullchain.pem', 'privkey.pem'))