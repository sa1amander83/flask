import os
import re
from datetime import datetime

import flask
import psycopg2
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
CORS(app)
app.secret_key = '412478680b3d5c11192483aaae6ea695035286f657da298c'
app.debug = True
messages = []

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db',
                            user="postgres",
                            password="root")
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
        email = "" if not email else email
        userage = request.form.get('age')
        password = request.form.get('password')
        register_date = datetime.now()


        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users;')
        users = cur.fetchall()

        for user in users:
            if user[0] == int(userid):
                messages.append('Пользователь с таким id уже есть в списке')
            if user[1] == username:
                messages.append('пользователь  с таким именем уже есть в списке')
            if user[4] == email:
                messages.append('пользователь c таким email уже есть в списке')

        if not userid:
            messages.append('Вы не ввели id пользователя')

            # flash('Вы не ввели id пользователя')
        if not username:
            # flash('Вы не ввели имя')
            messages.append('Вы не ввели имя')

        if not email:
            # flash('Вы не ввели email')
            messages.append('Вы не ввели email')

        if not userage:
            messages.append('Вы не ввели возраст')

            # flash('Вы не ввели возраст')
        if not password:
            messages.append('Вы не ввели пароль')
            # flash('Введите пароль')

            # else:
            #     return render_template('adduser.html', messages=messages)
            # return render_template('adduser.html', messages=messages)

        #     if check_password(password,messages):
        #         return render_template('adduser.html', messages=messages)
        #     else:
        #         return render_template('password.html', messages=messages)
        #
        # def check_password(password, messages):

        count = 0
        if len(password) < 8:
            messages.append('Длина пароля меньше 8 символов')
        else:
            count += 1
        if not bool(re.search('[A-ZА-Я]', password)):
            messages.append('пароль должен включать буквы верхнего регистра')
        else:
            count += 1
        if not bool(re.search('[a-zа-я]', password)):
            messages.append('пароль должен включать буквы нижнего регистра')
        else:
            count += 1
        if not bool(re.search('[0-9]', password)):
            messages.append('пароль должен включать цифры')
        else:
            count += 1
        if not bool(re.search('[!£$%&]', password)):
            messages.append('пароль должен включать хотя бы один специальный символ: !, £, $, %, &,')
        else:
            count += 1

        if count <= 2:
            messages.append('Пароль слишком слабый')
            return render_template('adduser.html', messages=messages)
        elif 2 < count < 5:
            flash('Пароль хороший, но недостаточно... Желаете улучшить пароль?')
            # form = """
            #        <form method="post" action="{{ url_for("checkpass") }}" id="passform">
            #     {#            <a href="{{ url_for('checkpass') }}" > yes</a>#}
            #     {#            <a href="{{ url_for('checkpass') }}" > no</a>#}
            #     <button type="submit" name="submit_button" value="yes"> ДА</button>
            #     <button type="submit" name="submit_button" value="no"> НЕТ</button>
            #     </form>
            #         """
            return render_template('adduser.html', messages=messages, passform=True)
        else:
            flash('Ваш пароль сильный!')
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT into users(id,name,age,password,email, date_register)'
                        'VALUES (%s, %s, %s, %s,%s,%s)',
                        (userid, username, userage, password, email, register_date)
                        )
            conn.commit()
            return render_template('success.html')


@app.route('/checkpass/', methods=['GET', 'POST'])
@cross_origin(origin='localhost', headers=['Content- Type', '*'])
def checkpass():
    userid = request.form.get('userid')
    username = request.form.get('username')
    email = request.form.get('email')
    userage = request.form.get('age')
    password = request.form.get('password')
    if request.method == 'POST':
        if request.form['submit_button'] == 'yes':
            return render_template('adduser.html', userid=userid)
        elif request.form['submit_button'] == 'no':
            pass


@app.route('/print/')
def print_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('print.html', users=users)


@app.route('/change/', methods=['GET', 'POST'])
@cross_origin(origin='localhost', headers=['Content- Type', '*'])
def change():
    if request.method == 'POST':
        username = request.form.get('username')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT name FROM users;')
        users = cur.fetchall()
        for user in users:
            print(user[0])
            if user[0] == username:
                return render_template('changepswd.html', change=True)
        else:
            flash("пользователь  с таким именем не найден, попробуйте еще раз")

        if request.form['submit_button'] == 'updatepass':
            return render_template('success.html', update=True)

    return render_template('changepswd.html')


@app.route('/quit/')
def quit():
    return render_template('quit.html')


if __name__ == '__main__':
    app.run()
