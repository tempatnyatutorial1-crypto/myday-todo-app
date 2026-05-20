import streamlit as st
import sqlite3

st.set_page_config(page_title="MyDay Todo", layout="centered")

DB = "todo.db"

conn = sqlite3.connect(DB, check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    category TEXT,
    priority TEXT
)
""")

conn.commit()

st.title("📝 MyDay To-Do App")

task = st.text_input("Task")

category = st.selectbox(
    "Category",
    ["My Day", "Work", "Travel", "Groceries"]
)

priority = st.selectbox(
    "Priority",
    ["High", "Medium", "Low"]
)

if st.button("Add Task"):

    if task:

        cur.execute(
            "INSERT INTO tasks(title, category, priority) VALUES(?,?,?)",
            (task, category, priority)
        )

        conn.commit()

        st.success("Task Added")

tasks = cur.execute(
    "SELECT * FROM tasks ORDER BY id DESC"
).fetchall()

st.subheader("Your Tasks")

for t in tasks:

    col1, col2 = st.columns([8,1])

    with col1:
        st.write(f"✅ {t[1]} — {t[2]} — {t[3]}")

    with col2:

        if st.button("❌", key=t[0]):

            cur.execute("DELETE FROM tasks WHERE id=?", (t[0],))
            conn.commit()

            st.rerun()