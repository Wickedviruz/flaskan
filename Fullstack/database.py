import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

c.execute('''CREATE TABLE users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              username TEXT NOT NULL, 
              email TEXT NOT NULL,
              name TEXT NOT NULL, 
              password TEXT NOT NULL)''')

c.execute('''CREATE TABLE tokens
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              user_id INTEGER NOT NULL, 
              token TEXT NOT NULL, 
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
              FOREIGN KEY (user_id) REFERENCES users (id))''')

conn.commit()

conn.close()