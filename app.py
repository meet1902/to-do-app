import streamlit as st
import sqlite3

# --- Database setup ---
conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pending'
    )
""")
conn.commit()

# --- Helper functions ---
def add_task(title):
    cursor.execute("INSERT INTO tasks (title, status) VALUES (?, ?)", (title, "Pending"))
    conn.commit()

def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()

def get_tasks_by_status(status):
    cursor.execute("SELECT * FROM tasks WHERE status = ?", (status,))
    return cursor.fetchall()

def mark_done(task_id):
    cursor.execute("UPDATE tasks SET status = 'Done' WHERE id = ?", (task_id,))
    conn.commit()

def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

# --- App UI ---
st.set_page_config(page_title="To-Do List", layout="centered")

st.markdown("""
    <style>
        .main-title {
            font-size: 40px;
            text-align: center;
            font-weight: bold;
            color: #3E64FF;
        }
        .task-card {
            background-color: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        }
        .task-title {
            font-size: 18px;
        }
        .task-done {
            color: green;
            font-weight: bold;
        }
        .task-pending {
            color: #ff6b6b;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>📝 My To-Do List</div>", unsafe_allow_html=True)

# --- Add Task ---
with st.form("Add Task"):
    new_task = st.text_input("Enter a new task", placeholder="Buy groceries, Learn Streamlit, etc.")
    submitted = st.form_submit_button("➕ Add Task")
    if submitted and new_task.strip():
        add_task(new_task.strip())
        st.success("Task added successfully!")
        st.experimental_rerun()

# --- Tabs ---
tab_labels = ["All", "Pending", "Done"]
tabs = st.tabs(tab_labels)

for i, tab in enumerate(tabs):
    with tab:
        if tab_labels[i] == "All":
            tasks = get_tasks()
        else:
            tasks = get_tasks_by_status(tab_labels[i])

        if not tasks:
            st.info("No tasks found here.")
        for task in tasks:
            task_id, title, status = task
            st.markdown(f"""
                <div class="task-card">
                    <span class="task-title">{title}</span><br>
                    <span class="{ 'task-done' if status == 'Done' else 'task-pending' }">Status: {status}</span>
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
