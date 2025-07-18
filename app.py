import streamlit as st
import sqlite3

# ----------------------- DB Functions -----------------------
conn = sqlite3.connect('tasks.db', check_same_thread=False)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        status TEXT DEFAULT 'Pending'
    )
''')
conn.commit()

def add_task(task):
    c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()

def get_tasks():
    c.execute("SELECT * FROM tasks")
    return c.fetchall()

def mark_done(task_id):
    c.execute("UPDATE tasks SET status='Done' WHERE id=?", (task_id,))
    conn.commit()

def delete_task(task_id):
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()

# --------------------- Page Setup --------------------------
st.set_page_config(page_title="📝 To-Do WebApp", layout="centered")

# -------------------- Custom CSS Styling -------------------
st.markdown("""
    <style>
        .title {
            font-size: 42px;
            font-weight: 800;
            color: #333;
            text-align: center;
        }
        .task-card {
            background-color: #f2f2f2;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .task-done {
            background-color: #d1e7dd !important;
            color: #155724;
            text-decoration: line-through;
        }
        .task-pending {
            background-color: #fff3cd !important;
            color: #856404;
        }
        .task-title {
            font-size: 18px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">📋 My To-Do List</div>', unsafe_allow_html=True)
st.markdown("### Add New Task:")

# ------------------ Input Form ------------------
with st.form("task_form", clear_on_submit=True):
    new_task = st.text_input("Task", placeholder="Enter your task here...")
    submitted = st.form_submit_button("➕ Add Task")
    if submitted and new_task.strip():
        add_task(new_task.strip())
        st.success(f"Task added: {new_task}")
        st.rerun()

# ------------------ Display Tasks ------------------
st.markdown("### 🗂️ Your Tasks:")
tasks = get_tasks()

if tasks:
    for i, task in enumerate(tasks):
        task_id, task_text, task_status = task
        bg_class = "task-card task-done" if task_status == "Done" else "task-card task-pending"
        
        st.markdown(f"""
            <div class="{bg_class}">
                <span class="task-title">{task_text}</span>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            if task_status != "Done":
                if st.button("✅ Mark Done", key=f"done_{task_id}_{i}"):
                    mark_done(task_id)
                    st.rerun()
        with col2:
            if st.button("❌ Delete", key=f"delete_{task_id}_{i}"):
                delete_task(task_id)
                st.rerun()
else:
    st.info("🎉 No tasks yet! Add your first task above.")
