from flask import Flask, render_template, request, redirect
import pymysql
import config

app = Flask(__name__)


def get_connection():
    conn = pymysql.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB
        )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(255) NOT NULL,
        department VARCHAR(100) NOT NULL)
    """)
    conn.commit()
    return conn
@app.route('/')
def index():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    conn.close()

    return render_template('index.html', employees=employees)


@app.route('/add', methods=['GET', 'POST'])
def add_employee():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        department = request.form['department']

        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO employees
            (name, email, department)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (name, email, department)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_user.html')


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )