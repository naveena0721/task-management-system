from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# =========================
# DATABASE
# =========================

def init_db():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # TASK TABLE
    cursor.execute('''

    CREATE TABLE IF NOT EXISTS tasks (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        task_name TEXT NOT NULL,

        status TEXT DEFAULT 'Pending'

    )

    ''')

    # PROFILE TABLE
    cursor.execute('''

    CREATE TABLE IF NOT EXISTS profile (

        id INTEGER PRIMARY KEY,

        name TEXT,

        email TEXT,

        password TEXT,

        preference TEXT

    )

    ''')

    # CHECK PROFILE EXISTS
    cursor.execute("SELECT * FROM profile")

    profile = cursor.fetchone()

    # INSERT DEFAULT PROFILE
    if not profile:

        cursor.execute("""

        INSERT INTO profile
        (name,email,password,preference)

        VALUES
        ('User',
         'user@gmail.com',
         '1234',
         'Daily Tasks')

        """)

    conn.commit()
    conn.close()

# RUN DATABASE
init_db()

# =========================
# LOGIN
# =========================

@app.route('/')
def login():
    return render_template('login.html')

# =========================
# SIGNUP
# =========================

@app.route('/signup')
def signup():
    return render_template('signup.html')

# =========================
# DASHBOARD
# =========================

@app.route('/dashboard')
def dashboard():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # TASKS
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    # COUNTS
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE status='Completed'"
    )

    completed_tasks = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE status='Pending'"
    )

    pending_tasks = cursor.fetchone()[0]

    # PROFILE
    cursor.execute(
        "SELECT * FROM profile WHERE id=1"
    )

    profile = cursor.fetchone()

    conn.close()

    return render_template(
        'dashboard.html',
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        profile=profile
    )

# =========================
# TASKS PAGE
# =========================

@app.route('/tasks')
def tasks():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    conn.close()

    return render_template(
        'tasks.html',
        tasks=tasks
    )

# =========================
# ADD TASK
# =========================

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():

    if request.method == 'POST':

        task = request.form['task']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tasks (task_name, status) VALUES (?, ?)",
            (task, 'Pending')
        )

        conn.commit()
        conn.close()

        return redirect('/tasks')

    return render_template('add_task.html')

# =========================
# EDIT TASK
# =========================

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        task_name = request.form['task']
        status = request.form['status']

        cursor.execute(
            "UPDATE tasks SET task_name=?, status=? WHERE id=?",
            (task_name, status, id)
        )

        conn.commit()
        conn.close()

        return redirect('/tasks')

    cursor.execute(
        "SELECT * FROM tasks WHERE id=?",
        (id,)
    )

    task = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_task.html',
        task=task
    )

# =========================
# COMPLETE TASK
# =========================

@app.route('/complete/<int:id>')
def complete(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status=? WHERE id=?",
        ("Completed", id)
    )

    conn.commit()
    conn.close()

    return redirect('/tasks')

# =========================
# COMPLETED PAGE
# =========================

@app.route('/completed')
def completed():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE status='Completed'"
    )

    tasks = cursor.fetchall()

    conn.close()

    return render_template(
        'completed.html',
        tasks=tasks
    )

# =========================
# CALENDAR PAGE
# =========================

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

# =========================
# REPORTS PAGE
# =========================

@app.route('/reports')
def reports():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # TOTAL TASKS
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]

    # COMPLETED TASKS
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Completed'")
    completed_tasks = cursor.fetchone()[0]

    # PENDING TASKS
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Pending'")
    pending_tasks = cursor.fetchone()[0]

    # OVERDUE TASKS
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Overdue'")
    overdue_tasks = cursor.fetchone()[0]

    # PRODUCTIVITY %
    productivity = 0

    if total_tasks > 0:
        productivity = int((completed_tasks / total_tasks) * 100)

    conn.close()

    return render_template(
        'reports.html',
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        overdue_tasks=overdue_tasks,
        productivity=productivity
    )

# =========================
# PROFILE PAGE
# =========================

@app.route('/profile', methods=['GET', 'POST'])
def profile():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        preference = request.form['preference']

        cursor.execute("""

        UPDATE profile
        SET name=?,
            email=?,
            password=?,
            preference=?
        WHERE id=1

        """,

        (name, email, password, preference)
        )

        conn.commit()

    cursor.execute(
        "SELECT * FROM profile WHERE id=1"
    )

    profile = cursor.fetchone()

    conn.close()

    return render_template(
        'profile.html',
        profile=profile
    )

# =========================
# DELETE TASK
# =========================

@app.route('/delete/<int:id>')
def delete_task(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/tasks')

# =========================
# RUN APP
# =========================

if __name__ == '__main__':
    app.run(debug=True)