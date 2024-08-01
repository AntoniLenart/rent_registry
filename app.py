from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['DATABASE'] = 'instance/devices.db'

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    rentals = conn.execute('SELECT * FROM rentals').fetchall()
    conn.close()
    
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('index.html', rentals=rentals, today_date=today_date)

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        device_id = request.form['device_id']
        email = request.form['email']
        rental_date = datetime.now().strftime('%Y-%m-%d')
        return_date = request.form['return_date']
        device_type = request.form['device_type']

        conn = get_db_connection()
        conn.execute('INSERT INTO rentals (device_id, email, rental_date, return_date, device_type) VALUES (?, ?, ?, ?, ?)',
                     (device_id, email, rental_date, return_date, device_type))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/return/<int:id>', methods=('POST',))
def return_device(id):
    conn = get_db_connection()
    rental = conn.execute('SELECT * FROM rentals WHERE id = ?', (id,)).fetchone()
    
    # Pobierz dzisiejszą datę jako datę zwrotu
    return_date = datetime.now().strftime('%Y-%m-%d')

    conn.execute('INSERT INTO history (device_id, email, rental_date, return_date, device_type) VALUES (?, ?, ?, ?, ?)',
                 (rental['device_id'], rental['email'], rental['rental_date'], return_date, rental['device_type']))
    conn.execute('DELETE FROM rentals WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/history')
def history():
    conn = get_db_connection()
    history = conn.execute('SELECT * FROM history').fetchall()
    conn.close()
    return render_template('history.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)
