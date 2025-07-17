import streamlit as st
import sqlite3
import os

# Page config
st.set_page_config(page_title="📝 To-Do List", page_icon="✅")

# Create database file
DB_FILE = "todo.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
c = conn.cursor()

# Create table if not exists
c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        status TEXT DEFAULT 'Pending'
    )
""")
conn.commit()

# Functions
def get_tasks():
    c.execute("SELECT * FROM tasks")
    return c.fetchall()

def add_task(task):
    c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()

def mark_done(task_id):
    c.execute("UPDATE tasks SET status='Done' WHERE id=?", (task_id,))
    conn.commit()

def delete_task(task_id):
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()

# UI
st.title("📝 To-Do List")

# Add task form
with st.form("add_task_form"):
    task_input = st.text_input("Enter a new task:")
    submitted = st.form_submit_button("Add")
    if submitted:
        if task_input.strip():
            add_task(task_input.strip())
            st.success("Task added!")
            st.rerun()
        else:
            st.warning("Task cannot be empty.")

# Show tasks
tasks = get_tasks()
if tasks:
    for task in tasks:
        col1, col2, col3 = st.columns([6, 1, 1])
        task_text = f"~~{task[1]}~~ ✅" if task[2] == "Done" else f"{task[1]}"
        col1.markdown(task_text)
        
        if task[2] != "Done":
            if col2.button("✅", key=f"done_{task[0]}"):
                mark_done(task[0])
                st.rerun()
        
        if col3.button("❌", key=f"delete_{task[0]}"):
            delete_task(task[0])
            st.rerun()
else:
    st.info("No tasks found. Add one above.")
