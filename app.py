import streamlit as st
import sqlite3

# Set up the page
st.set_page_config(page_title="📝 To-Do List", page_icon="✅", layout="centered")

# Connect to SQLite database (auto-creates the file)
conn = sqlite3.connect("tasks.db", check_same_thread=False)
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        status TEXT DEFAULT 'Pending'
    )
''')
conn.commit()

# Add task
def add_task(task):
    c.execute("INSERT INTO tasks (task, status) VALUES (?, 'Pending')", (task,))
    conn.commit()

# Get tasks
def get_tasks():
    c.execute("SELECT * FROM tasks")
    return c.fetchall()

# Mark task as done
def mark_done(task_id):
    c.execute("UPDATE tasks SET status='Done' WHERE id=?", (task_id,))
    conn.commit()

# Delete task
def delete_task(task_id):
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()

# UI
st.title("📝 My To-Do List")
st.markdown("Stay organized and productive.")

# Add task form
with st.form("Add Task"):
    task_input = st.text_input("Enter a new task")
    submitted = st.form_submit_button("Add")
    if submitted and task_input.strip():
        add_task(task_input.strip())
        st.success("Task added successfully!")
        st.experimental_rerun()

# Show tasks
tasks = get_tasks()
if tasks:
    for task in tasks:
        col1, col2, col3 = st.columns([6, 1, 1])
        status = "✅" if task[2] == "Done" else "🔄"
        col1.markdown(f"**{task[1]}** &nbsp; {status}")
        if task[2] == "Pending":
            if col2.button("Done", key=f"done_{task[0]}"):
                mark_done(task[0])
                st.experimental_rerun()
        if col3.button("Delete", key=f"delete_{task[0]}"):
            delete_task(task[0])
            st.experimental_rerun()
else:
    st.info("No tasks yet. Add one above!")

