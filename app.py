import streamlit as st

# Page config
st.set_page_config(page_title="📝 To-Do List", page_icon="✅")

# Initialize task list
if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.title("📝 To-Do List")
st.write("Add, complete, or remove your tasks easily.")

# Add Task
task = st.text_input("New task", "")
if st.button("Add Task"):
    if task:
        st.session_state.tasks.append({"task": task, "done": False})
        st.success(f"Added: {task}")
    else:
        st.warning("Please enter a task.")

# Show Tasks
if st.session_state.tasks:
    for i, t in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([6, 1, 1])
        col1.markdown(f"{'✅ ' if t['done'] else '🔘 '} **{t['task']}**" if not t['done'] else f"~~{t['task']}~~ ✅")

        if not t["done"]:
            if col2.button("Done", key=f"done{i}"):
                st.session_state.tasks[i]["done"] = True
                st.rerun()

        if col3.button("❌", key=f"del{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()
else:
    st.info("No tasks yet.")
