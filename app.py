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
    def succsses():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT into users(id,name,age,password,email, date_register)'
                    'VALUES (%s, %s, %s, %s,%s,%s)',
                    (userid, username, userage, password, email, register_date)
                    )

        conn.commit()

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
        # if request.form['submit_button'] == 'no':
        #     succsses()
        try:
            if request.form['submit_button'] == 'no':
                succsses()
                return render_template('success.html')
        except:
            pass

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

        if check(password) <= 2:
            messages.append('Пароль слишком слабый')
            return render_template('adduser.html', messages=messages)
        elif 2 < check(password) < 5:
            flash('Пароль хороший, но недостаточно... Желаете улучшить пароль?')

            return render_template('adduser.html', messages=messages, passform=True)
        else:
            flash('Ваш пароль сильный!')
            succsses()
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
            print(1321)

    return render_template('adduser.html', userid=userid)


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
    if request.method == 'GET':
        return render_template('changepswd.html')

    # username=None
    if request.method == 'POST':
        username = request.form.get('username')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT name FROM users;')
        users = cur.fetchall()

        for user in users:

            if user[0] == username:


                return render_template('changepswd.html', change=True, user=user[0])

        else:
            flash("пользователь  с таким именем не найден, попробуйте еще раз")
            return render_template('changepswd.html')


@app.route('/updatepass/<string:username>', methods=['GET', 'POST'])
@cross_origin(origin='localhost', headers=['Content- Type', '*'])
def updatepass(username):
    newpass = request.form.get('updatepass')
    if request.method == 'POST':
        print(request.form)
        if check(newpass) == 5 or request.form['button_submit'] == 'no':
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("UPDATE users SET password = %s WHERE name = %s;", (newpass, username,))
            conn.commit()
            conn.close()
            return render_template('success.html', update=True)
        elif request.form['button_submit'] == 'yes':
            return render_template('changepswd.html', change=True,user=username,  password=newpass)

        elif check(newpass) <= 2:
            flash('Пароль слишком слабый')
            return render_template('changepswd.html', change=True, user=username, password=newpass)
        elif 2 < check(newpass) < 5:
            flash('Пароль хороший, но недостаточно... Желаете улучшить пароль?')
            return render_template('changepswd.html', update=True, change=True,user=username, password=newpass)


@app.route('/quit/')
def quit():
    return render_template('quit.html')


def check(password):
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
    return count


if __name__ == '__main__':
    app.run()
