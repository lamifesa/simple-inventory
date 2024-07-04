from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nicetomeetyou'

# conncts the db to the app
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_data(employ_id):
    conn = get_db_connection()
    employee = conn.execute('SELECT * FROM employee WHERE id = ?',
                (employ_id,)).fetchone()
    conn.close()
    if employee is None:
        abort(404)
    return employee

# Display employee directory
@app.route('/')
@app.route('/index')
def index():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM employee').fetchall()
    conn.close()
    return render_template('index.html', data=data)


@app.route('/input.html', methods=('GET', 'POST'))
def input():
    if request.method == 'POST':
        fname = request.form['fname'].lower()
        lname = request.form['lname'].lower()
        sex = request.form['sex'].lower()
        job = request.form['job'].lower()

        conn = get_db_connection()
        conn.execute('INSERT INTO employee(fname, lname, sex, job) VALUES(?, ?, ?, ?)', (fname, lname, sex, job))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('input.html')

@app.route('/<int:id>/edit.html', methods=('GET', 'POST'))
def edit(id):
    employ = get_data(id)

    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        sex = request.form['sex']
        job = request.form['job']

        conn = get_db_connection()
        conn.execute('UPDATE employee SET fname= ?, lname = ?, sex = ?, job=? WHERE id = ?', (fname, lname, sex, job, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('edit.html', employ=employ)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    employee = get_data(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM employee WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)