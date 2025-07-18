import streamlit as st
import sqlite3
from datetime import datetime

# --- Database Setup ---
conn = sqlite3.connect('tasks.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pending'
    )
''')
conn.commit()

# --- App UI Setup ---
st.set_page_config(page_title="📝 To-Do List App", layout="centered")
st.title("📝 Elegant To-Do List")

menu = ["All Tasks", "Pending Tasks", "Completed Tasks"]
choice = st.sidebar.radio("View", menu)

# --- Add New Task ---
st.subheader("➕ Add New Task")
new_task = st.text_input("Enter a task", placeholder="e.g., Buy groceries")
if st.button("Add Task"):
    if new_task.strip():
        cursor.execute("INSERT INTO tasks (title, status) VALUES (?, 'Pending')", (new_task.strip(),))
        conn.commit()
        st.success("Task added successfully!")
        st.experimental_rerun()

# --- View Tasks ---
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()

def update_status(task_id, new_status):
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    st.experimental_rerun()

def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    st.experimental_rerun()

all_tasks = get_tasks()

if choice == "All Tasks":
    st.subheader("📋 All Tasks")
    for idx, task in enumerate(all_tasks):
        col1, col2, col3 = st.columns([6, 2, 2])
        with col1:
            st.write(f"{task[1]} ({task[2]})")
        with col2:
            if st.button("✅ Done" if task[2] == 'Pending' else "↩️ Undo", key=f"done_{task[0]}_{idx}"):
                update_status(task[0], 'Done' if task[2] == 'Pending' else 'Pending')
        with col3:
            if st.button("🗑️ Delete", key=f"delete_{task[0]}_{idx}"):
                delete_task(task[0])

elif choice == "Pending Tasks":
    st.subheader("🕓 Pending Tasks")
    for idx, task in enumerate(all_tasks):
        if task[2] == 'Pending':
            col1, col2, col3 = st.columns([6, 2, 2])
            with col1:
                st.write(task[1])
            with col2:
                if st.button("✅ Done", key=f"done_pending_{task[0]}_{idx}"):
                    update_status(task[0], 'Done')
            with col3:
                if st.button("🗑️ Delete", key=f"delete_pending_{task[0]}_{idx}"):
                    delete_task(task[0])

elif choice == "Completed Tasks":
    st.subheader("✅ Completed Tasks")
    for idx, task in enumerate(all_tasks):
        if task[2] == 'Done':
            col1, col2, col3 = st.columns([6, 2, 2])
            with col1:
                st.write(task[1])
            with col2:
                if st.button("↩️ Undo", key=f"undo_done_{task[0]}_{idx}"):
                    update_status(task[0], 'Pending')
            with col3:
                if st.button("🗑️ Delete", key=f"delete_done_{task[0]}_{idx}"):
                    delete_task(task[0])
