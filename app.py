import streamlit as st
import sqlite3

# Page Setup
st.set_page_config(page_title="🧠 Smart Tasks", page_icon="✅", layout="centered")

# Connect DB
conn = sqlite3.connect("todo.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, status TEXT DEFAULT 'Pending')")
conn.commit()

# Styling
st.markdown("""
    <style>
        .task-card {
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 10px;
            background: linear-gradient(to right, #f8fafc, #f1f5f9);
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .task-done {
            background: linear-gradient(to right, #d1fae5, #a7f3d0);
            text-decoration: line-through;
        }
        .task-pending {
            background: linear-gradient(to right, #fef9c3, #fde68a);
        }
        .task-title {
            font-size: 18px;
            font-weight: 600;
            color: #111827;
        }
    </style>
""", unsafe_allow_html=True)

# Functions
def add_task(task):
    c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()

def get_tasks(status_filter=None):
    if status_filter:
        c.execute("SELECT * FROM tasks WHERE status=?", (status_filter,))
    else:
        c.execute("SELECT * FROM tasks")
    return c.fetchall()

def mark_done(task_id):
    c.execute("UPDATE tasks SET status='Done' WHERE id=?", (task_id,))
    conn.commit()

def delete_task(task_id):
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()

# Sidebar
with st.sidebar:
    st.title("📊 Task Summary")
    total = len(get_tasks())
    done = len(get_tasks("Done"))
    pending = len(get_tasks("Pending"))
    st.metric("Total", total)
    st.metric("✅ Done", done)
    st.metric("🔄 Pending", pending)

# Title
st.title("🧠 Smart Tasks")
st.subheader("Manage your day like a pro.")

# Add Task
with st.form("add_task"):
    new_task = st.text_input("What's on your mind?")
    submitted = st.form_submit_button("Add ➕")
    if submitted and new_task.strip():
        add_task(new_task.strip())
        st.success("Task added!")
        st.rerun()

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 All", "🔄 Pending", "✅ Done"])

def render_tasks(tasks):
    for task in tasks:
        bg_class = "task-card task-done" if task[2] == "Done" else "task-card task-pending"
        st.markdown(f"""
            <div class="{bg_class}">
                <span class="task-title">{task[1]}</span>
                <div>
                    {'<button onclick="window.location.reload()" style="margin-right:10px">✅</button>' if task[2] != 'Done' else ''}
                    <form action="" method="post" style="display:inline">
                        <button style="background:red;color:white;border:none;border-radius:5px;" onclick="window.location.reload()">❌</button>
                    </form>
                </div>
            </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            if task[2] != "Done":
                if st.button("✅ Mark Done", key=f"done_{task[0]}"):
                    mark_done(task[0])
                    st.rerun()
        with col2:
            if st.button("❌ Delete", key=f"del_{task[0]}"):
                delete_task(task[0])
                st.rerun()

with tab1:
    render_tasks(get_tasks())

with tab2:
    render_tasks(get_tasks("Pending"))

with tab3:
    render_tasks(get_tasks("Done"))
