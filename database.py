import sqlite3

def init_db():
    conn = sqlite3.connect('college.db')
    cur = conn.cursor()

    # Admin table
    cur.execute('''CREATE TABLE IF NOT EXISTS admin (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT)''')

    # Student table
    cur.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    course TEXT)''')

    # Course table
    cur.execute('''CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    description TEXT)''')

    # Enrollment table
    cur.execute('''CREATE TABLE IF NOT EXISTS enrollments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    course_id INTEGER,
                    FOREIGN KEY(student_id) REFERENCES students(id),
                    FOREIGN KEY(course_id) REFERENCES courses(id))''')

    # Default admin
    cur.execute("INSERT OR IGNORE INTO admin (username, password) VALUES ('admin', 'admin123')")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
