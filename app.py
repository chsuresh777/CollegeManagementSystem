from flask import Flask, render_template, request, redirect, session
import sqlite3
from database import init_db

app = Flask(__name__)
app.secret_key = "supersecretkey"
init_db()

def get_db():
    return sqlite3.connect('college.db')

@app.route('/')
def home():
    return redirect('/login')

# --- LOGIN ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin WHERE username=? AND password=?", (uname, pwd))
        admin = cur.fetchone()
        conn.close()
        if admin:
            session['admin'] = uname
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid Credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/login')

# --- DASHBOARD ---
@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect('/login')
    return render_template('dashboard.html')

# --- STUDENTS ---
@app.route('/students')
def students():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    conn.close()
    return render_template('students.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    email = request.form['email']
    course = request.form['course']
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, email, course) VALUES (?, ?, ?)", (name, email, course))
    conn.commit()
    conn.close()
    return redirect('/students')

@app.route('/delete_student/<int:id>')
def delete_student(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/students')

# --- COURSES ---
@app.route('/courses')
def courses():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses")
    courses = cur.fetchall()
    conn.close()
    return render_template('courses.html', courses=courses)

@app.route('/add_course', methods=['POST'])
def add_course():
    name = request.form['name']
    desc = request.form['description']
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO courses (name, description) VALUES (?, ?)", (name, desc))
    conn.commit()
    conn.close()
    return redirect('/courses')

@app.route('/delete_course/<int:id>')
def delete_course(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM courses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/courses')

# --- ENROLLMENTS ---
@app.route('/enrollments')
def enrollments():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""SELECT e.id, s.name, c.name 
                   FROM enrollments e
                   JOIN students s ON e.student_id=s.id
                   JOIN courses c ON e.course_id=c.id""")
    data = cur.fetchall()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.execute("SELECT * FROM courses")
    courses = cur.fetchall()
    conn.close()
    return render_template('enrollments.html', data=data, students=students, courses=courses)

@app.route('/add_enrollment', methods=['POST'])
def add_enrollment():
    sid = request.form['student_id']
    cid = request.form['course_id']
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (sid, cid))
    conn.commit()
    conn.close()
    return redirect('/enrollments')
if __name__ == '__main__':
    app.run(debug=True)

