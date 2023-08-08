from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = '12345'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?,?)', (username, password))
            conn.commit()
            conn.close()
            flash('Usuário criado com sucesso!')
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password =?', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['username'] = user[1]
            flash('Login realizado com sucesso!')
            return redirect(url_for('perfil'))
        else:
            return 'Usuário ou senha incorretos.'

@app.route('/perfil')
def perfil():
      if 'username' in session:
        username = session['username']
        return render_template('perfil.html', username=username)
      else:
            return redirect(url_for('index'))
      

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
     

def init_db():
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
init_db()


if __name__ == '__main__':
    app.run(debug=True)


