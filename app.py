import streamlit as st

st.set_page_config(page_title="📝 To-Do List", page_icon="✅", layout="centered")

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Title
st.title("📝 My To-Do List")
st.markdown("Stay organized and productive.")

# Add Task
with st.form("task_form"):
    new_task = st.text_input("Enter a new task", "")
    submitted = st.form_submit_button("Add")
    if submitted and new_task.strip():
        st.session_state.tasks.append({"task": new_task.strip(), "done": False})
        st.success("Task added!")

# Show Tasks
if st.session_state.tasks:
    for i, t in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([6, 1, 1])
        task_text = f"~~{t['task']}~~ ✅" if t["done"] else t["task"]
        col1.markdown(f"**{task_text}**")
        if not t["done"]:
            if col2.button("Done", key=f"done{i}"):
                st.session_state.tasks[i]["done"] = True
                st.experimental_rerun()
        if col3.button("Delete", key=f"delete{i}"):
            st.session_state.tasks.pop(i)
            st.experimental_rerun()
else:
    st.info("No tasks yet. Add one above!")
