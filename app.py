from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'api'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    student = cur.fetchall()
    cur.close()

    return render_template('index.html', student=student)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        std_name = request.form['std_name']
        major = request.form['major']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student (std_id, std_name, major) VALUES (%s, %s, %s)", (std_name, major))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(std_id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        std_name = request.form['std_name']
        major = request.form['major']
        cur.execute("UPDATE student SET std_name=%s, major=%s WHERE std_id=%s", (std_name, major, std_id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))
    else:
        cur.execute("SELECT * FROM student WHERE std_id= %s", (std_id,))
        student = cur.fetchone()
        cur.close()

        return render_template('edit_add.html', student=student)

@app.route('/delete/<int:id>')
def delete(std_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM student WHERE std_id= %s", (std_id))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))

if __name__ == '_main_':
    app.run(debug=True)