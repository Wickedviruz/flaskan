from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
import os
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "'#\xd2\xa3\xb1\xdc<\xeb\xa5<-\xbf7?\x1d\xb5{'")
app.config['BCRYPT_LOG_ROUNDS'] = 12
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_DEFAULT_SENDER'] = 'johan.ivarsson@live.se'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'a66bc41c77a384'
app.config['MAIL_PASSWORD'] = 'b8f9f9362fe047'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['DATABASE'] = os.path.join(app.root_path, 'database.db')

login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)
bcrypt = Bcrypt(app)

class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id=?', (user_id,))
    result = c.fetchone()
    user = None
    if result:
        user = User(result[0], result[1], result[2])
    conn.close()
    return user

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email=?', (email,))
        result = c.fetchone()
        conn.close()
        if not result:
            flash('Invalid email or password.', 'error')
        elif not bcrypt.check_password_hash(result[4], password):
            flash('Invalid email or password.', 'error')
        else:
            user = User(result[0], result[2], result[4])
            login_user(user)
            session['logged_in'] = True
            session['email'] = email
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session and session['logged_in']:
        email = session['email']
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute('SELECT name FROM users WHERE email=?', (email,))
        result = c.fetchone()
        conn.close()
        if result:
            return render_template('dashboard.html', message='Welcome back, {}!'.format(result[0]))
        else:
            return render_template('dashboard.html', message='Welcome back!')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match.')
        else:
            conn = sqlite3.connect(app.config['DATABASE'])
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE email=?', (email,))
            result = c.fetchone()
            if result:
                flash('Email address already registered.')
            else:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                c.execute('INSERT INTO users (username, email, name, password) VALUES (?, ?, ?, ?)', (username, email, name, hashed_password))
                conn.commit()
                conn.close()
                flash('Registration successful.')
                return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email=?', (email,))
        result = c.fetchone()
        conn.close()
        if result:
            user_id = result[0]
            token = bcrypt.generate_password_hash(str(user_id)).decode('utf-8')
            reset_url = url_for('reset_password', token=token, _external=True)
            msg = Message(subject='Reset Your Password', recipients=[email])
            msg.body = f'To reset your password, click on this link: {reset_url}'
            mail.connect() # connect to mail server
            mail.send(msg)
            mail.disconnect() # disconnect from mail server
        flash('If an account with that email exists, we have sent you an email with instructions to reset your password.')
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        user_id = int(bcrypt.check_password_hash(token, token))
    except:
        flash('Invalid or expired token.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match.')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            conn = sqlite3.connect(app.config['DATABASE'])
            c = conn.cursor()
            c.execute('UPDATE users SET password=? WHERE id=?', (hashed_password, user_id))
            conn.commit()
            conn.close()
            flash('Password reset successfully.')
            return redirect(url_for('login'))
    return render_template('reset_password.html')


if __name__ == '__main__':
    app.run(debug=True)