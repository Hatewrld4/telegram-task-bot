import sqlite3

conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    task TEXT
)
""")
conn.commit()

def add_task(user_id, task):
    cursor.execute("INSERT INTO tasks (user_id, task) VALUES (?, ?)", (user_id, task))
    conn.commit()

def get_tasks(user_id):
    cursor.execute("SELECT id, task FROM tasks WHERE user_id=?", (user_id,))
    return cursor.fetchall()

def delete_task(user_id, task_id):
    cursor.execute("DELETE FROM tasks WHERE user_id=? AND id=?", (user_id, task_id))
    conn.commit()