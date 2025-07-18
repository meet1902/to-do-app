import streamlit as st
import sqlite3

# --- Database Setup ---
conn = sqlite3.connect('tasks.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pending'
    )
""")
conn.commit()

# --- Helper Functions ---
def add_task(title):
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()

def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()

def mark_done(task_id):
    cursor.execute("UPDATE tasks SET status='Done' WHERE id=?", (task_id,))
    conn.commit()

def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()

# --- UI Styling ---
st.set_page_config(page_title="Elegant To-Do App", layout="centered")
st.markdown("""
    <style>
        .main-title {
            font-size: 3em;
            text-align: center;
            margin-bottom: 20px;
            color: #4A90E2;
        }
        .task-card {
            padding: 10px;
            margin: 10px 0;
            border-radius: 8px;
            background-color: #f0f2f6;
        }
        .task-done {
            background-color: #d4edda;
            text-decoration: line-through;
        }
        .task-pending {
            background-color: #fff3cd;
        }
        .task-title {
            font-size: 18px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>📝 Elegant To-Do List</div>", unsafe_allow_html=True)

# --- Add Task ---
with st.form("Add Task"):
    task_input = st.text_input("Enter a task")
    submitted = st.form_submit_button("Add")
    if submitted and task_input:
        add_task(task_input)
        st.success("Task added successfully!")
        st.experimental_rerun()

# --- Task View Tabs ---
tab_labels = ["All", "Pending", "Done"]
tabs = st.tabs(tab_labels)
tasks = get_tasks()

for i, tab in enumerate(tabs):
    with tab:
        for idx, task in enumerate(tasks):
            task_id, title, status = task

            if tab_labels[i] == "Pending" and status != "Pending":
                continue
            if tab_labels[i] == "Done" and status != "Done":
                continue

            css_class = "task-done" if status == "Done" else "task-pending"
            st.markdown(f"""
                <div class='task-card {css_class}'>
                    <span class='task-title'>{title}</span>
                </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 1])
            with col1:
                if status != "Done":
                    if st.button("✅ Mark Done", key=f"done_{task_id}_{tab_labels[i]}"):
                        mark_done(task_id)
                        st.experimental_rerun()
            with col2:
                if st.button("❌ Delete", key=f"delete_{task_id}_{tab_labels[i]}"):
                    delete_task(task_id)
                    st.experimental_rerun()
