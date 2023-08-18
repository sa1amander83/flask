import os

import flask
import psycopg2
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
CORS(app)
app.secret_key = '412478680b3d5c11192483aaae6ea695035286f657da298c'


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db',
                            user="postgres",
                            password="123")
    return conn


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/adduser/')
def adduser():
    # addUserForm=request.form['addUserForm']
    return render_template('adduser.html')


@app.route('/adduserform/', methods=['POST', 'GET'])
@cross_origin(origin='localhost', headers=['Content- Type', '*'])
def adduserform():
    response = flask.jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'POST':

        userid = request.form.get('userid')
        username = request.form.get('username')
        email = request.form.get('email')
        userage = request.form.get('age')
        password = request.form.get('password')

        # обработка пароля
        if not userid:
            flash('Вы не ввели id пользователя')
        elif not username:
            flash('Вы не ввели имя')
        elif not email:
            flash('Вы не ввели email')
        elif not userage:
            flash('Вы не ввели возраст')
        elif not password:
            flash('Введите пароль')

        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM users;')
            users = cur.fetchall()
            for user in users:
                if user[1] == userid:
                    flash('Пользователь с таким id уже есть в списке')
                elif user[2] == username:
                    flash('Такой пользователь уже есть в списке')
                elif user[3] == email:
                    flash('пользователь c таким email уже есть в списке')

            return render_template('adduser.html')


@app.route('/print/')
def print_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('print.html', users=users)


@app.route('/change/')
def change():
    return render_template('changepswd.html')


@app.route('/quit/')
def quit():
    return render_template('quit.html')


if __name__ == '__main__':
    app.run()
