import streamlit as st
import sqlite3

# Initialize DB
conn = sqlite3.connect('tasks.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, status TEXT)")
conn.commit()

st.set_page_config(page_title="📝 To-Do List", page_icon="📝")

st.title("📝 My To-Do List")
st.markdown("Add your daily tasks and track them easily.")

# Add Task
with st.form(key='add_form'):
    new_task = st.text_input("Enter a new task")
    submit = st.form_submit_button("➕ Add Task")
    if submit and new_task:
        cursor.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (new_task, "Pending"))
        conn.commit()
        st.success("Task added!")

# Display Tasks
cursor.execute("SELECT * FROM tasks")
tasks = cursor.fetchall()

if tasks:
    for task in tasks:
        col1, col2, col3 = st.columns([6, 2, 2])
        status = "✅" if task[2] == "Done" else "❌"
        col1.write(f"**{task[1]}** {'(Done)' if task[2]=='Done' else ''}")
        if task[2] == "Pending":
            if col2.button("Mark Done", key=f"done{task[0]}"):
                cursor.execute("UPDATE tasks SET status='Done' WHERE id=?", (task[0],))
                conn.commit()
                st.experimental_rerun()
        if col3.button("Delete", key=f"del{task[0]}"):
            cursor.execute("DELETE FROM tasks WHERE id=?", (task[0],))
            conn.commit()
            st.experimental_rerun()
else:
    st.info("No tasks yet!")

