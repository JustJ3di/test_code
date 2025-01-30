from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # **IMPORTANT:** Replace with a strong, randomly generated secret key

# Database setup (example using SQLite)
DATABASE = 'users.db'

def create_db():
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        db.commit()

create_db() # Create the database if it doesn't exist

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')  # Create a login.html template

@app.route('/do_login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username =?", (username,))
        result = cursor.fetchone()

    if result:
        stored_password_hash = result
        if check_password_hash(stored_password_hash, password):  # Use Werkzeug for password hashing
            # Successful login
            return redirect(url_for('user_page', username=username)) # Pass username for user-specific pages
        else:
            flash('Incorrect password')  # Flash error message to the user
            return redirect(url_for('login')) # Redirect back to login
    else:
        flash('Username not found') # Flash error message to the user
        return redirect(url_for('login')) # Redirect back to login


@app.route('/user_page/<username>')  # Example user page
def user_page(username):
    return render_template('user_page.html', username=username) # Create a user_page.html template


# Example of how to add a user (do this securely, perhaps in a separate admin area)
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256') # Hash the password

    try:
        with sqlite3.connect(DATABASE) as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?,?)", (username, hashed_password))
            db.commit()
        return redirect(url_for('login')) # Redirect to login after registration
    except sqlite3.IntegrityError: # Handle duplicate usernames
        flash('Username already exists')
        return redirect(url_for('login')) # Redirect back to login


if __name__ == '__main__':
    app.run(debug=True) # Set debug=False in production!