import webbrowser
import threading
from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
app = Flask(__name__)
def get_db_connection():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS expenses
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     amount REAL NOT NULL,
                     category TEXT NOT NULL,
                     description TEXT,
                     date TEXT NOT NULL)''')
    conn.commit()
    conn.close()
init_db()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/add_expense', methods=['POST'])

def add_expense():
    data = request.get_json()
    amount = data['amount']
    category = data['category']
    description = data['description']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = get_db_connection()
    conn.execute('INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)',
                 (amount, category, description, date))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success'})
@app.route('/get_expenses')
def get_expenses():
    conn = get_db_connection()
    expenses = conn.execute('SELECT * FROM expenses ORDER BY date DESC').fetchall()
    conn.close()
    
    expenses_list = []
    for expense in expenses:
        expenses_list.append(dict(expense))
    
    return jsonify(expenses_list)
@app.route('/delete_expense/<int:id>', methods=['DELETE'])

def delete_expense(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    # Open the browser automatically after 1 second
    threading.Timer(1, lambda: webbrowser.open_new("http://127.0.0.1:5000")).start()
    app.run(debug=True)
