from flask import Flask, render_template, request, redirect, make_response, flash
from datetime import datetime

import sqlite3
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Для использования flash сообщений

def get_db_connection():
    conn = sqlite3.connect('messages.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Проверка существования таблицы
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
    if not cursor.fetchone():  # Если таблица не существует
        cursor.execute('''CREATE TABLE messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            message TEXT,
            ip TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        ip = request.remote_addr
        
        # Ограничение на длину сообщения
        if len(message) > 500:  # Замените 500 на нужное вам значение
            flash('Сообщение не должно превышать 500 символов.')
            return redirect('/')

        conn = get_db_connection()
        conn.execute('INSERT INTO messages (name, message, ip) VALUES (?, ?, ?)', (name, message, ip))
        conn.commit()
        conn.close()
        
        resp = make_response(redirect('/'))
        resp.set_cookie('name', name)
        return resp

    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY id DESC').fetchall()
    conn.close()

    return render_template('index.html', messages=messages, name=request.cookies.get('name', ''))

@app.route('/messages')
def messages():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY id DESC').fetchall()
    conn.close()
    
    formatted_messages = []
    for message in messages:
        formatted_message = {
            'id': message['id'],
            'name': message['name'],
            'message': message['message'],
            'ip': message['ip'],
            'timestamp': datetime.strptime(message['timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y %H:%M:%S')
        }
        formatted_messages.append(formatted_message)

    return render_template('messages.html', messages=formatted_messages)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000, debug=True)
