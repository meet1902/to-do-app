import streamlit as st
import sqlite3

# ---------------- Database Setup ----------------
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

def get_tasks(status=None):
    if status:
        c.execute("SELECT * FROM tasks WHERE status=?", (status,))
    else:
        c.execute("SELECT * FROM tasks")
    return c.fetchall()

def mark_done(task_id):
    c.execute("UPDATE tasks SET status='Done' WHERE id=?", (task_id,))
    conn.commit()

def delete_task(task_id):
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()

# ---------------- Streamlit Setup ----------------
st.set_page_config(page_title="📝 To-Do App", layout="centered")

# ---------------- CSS Styling ----------------
st.markdown("""
    <style>
        .title {
            font-size: 42px;
            font-weight: 800;
            color: #333;
            text-align: center;
        }
        .task-card {
            background-color: #f0f2f6;
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
        .stTabs [data-baseweb="tab-list"] {
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- Main UI ----------------
st.markdown('<div class="title">📋 To-Do List</div>', unsafe_allow_html=True)

# --- Add Task Form ---
st.markdown("### ➕ Add New Task")
with st.form("add_task", clear_on_submit=True):
    new_task = st.text_input("Task", placeholder="Enter task here...")
    submit = st.form_submit_button("Add Task")
    if submit and new_task.strip():
        add_task(new_task.strip())
        st.success("Task added successfully!")
        st.rerun()

# --- Tabs for All / Pending / Completed ---
tabs = st.tabs(["📋 All Tasks", "🕒 Pending", "✅ Completed"])

tab_labels = ["All", "Pending", "Done"]
for i, tab in enumerate(tabs):
    with tab:
        if tab_labels[i] == "All":
            tasks = get_tasks()
        else:
            tasks = get_tasks("Pending" if tab_labels[i] == "Pending" else "Done")

        if not tasks:
            st.info("No tasks here.")
        else:
            for idx, task in enumerate(tasks):
                task_id, task_text, task_status = task
                style_class = "task-done" if task_status == "Done" else "task-pending"
                st.markdown(f'''
                    <div class="task-card {style_class}">
                        <div class="task-title">{task_text}</div>
                    </div>
                ''', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1])
                with col1:
                    if task_status == "Pending":
                        if st.button("✅ Mark Done", key=f"done_{task_id}_{idx}"):
                            mark_done(task_id)
                            st.rerun()
                with col2:
                    if st.button("❌ Delete", key=f"delete_{task_id}_{idx}"):
                        delete_task(task_id)
                        st.rerun()
