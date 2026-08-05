import os
import streamlit as st
from sqlalchemy import create_engine, text
from databricks.sdk import WorkspaceClient

st.set_page_config(page_title="SyncMetrics Support Core", layout="wide")

# Read connection details from environment variables
# Secrets from resources are injected with the resource name (with hyphens)
DB_HOST = os.environ.get("lakebase-host", "localhost")
DB_PASSWORD = os.environ.get("lakebase-password", "password")
DB_PORT = os.environ.get("LAKEBASE_PORT", "5432")
DB_NAME = os.environ.get("LAKEBASE_DATABASE", "databricks_postgres")
DB_USER = os.environ.get("LAKEBASE_USER", "ticket-app-role")

# Construct the connection URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
engine = create_engine(DATABASE_URL)
st.title("🛠️ SyncMetrics Internal Support Dashboard")

# BONUS: Ticket statistics summary cards
with engine.connect() as conn:
    total_t = conn.execute(text("SELECT COUNT(*) FROM tickets")).scalar()
    open_t = conn.execute(text("SELECT COUNT(*) FROM tickets WHERE status='open'")).scalar()
    prog_t = conn.execute(text("SELECT COUNT(*) FROM tickets WHERE status='in_progress'")).scalar()

col1, col2, col3 = st.columns(3)
col1.metric("Total System Tickets", total_t)
col2.metric("🟢 Open Tickets", open_t)
col3.metric("🟡 In Progress", prog_t)
st.markdown("---")

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("📋 Active System Tickets")
    # BONUS: Filtering capabilities by ticket status
    status_filter = st.selectbox("Filter Tickets by Current Status", ["All", "open", "in_progress", "resolved"])

    query = "SELECT * FROM tickets"
    if status_filter != "All":
        query += f" WHERE status = '{status_filter}'"

    with engine.connect() as conn:
        tickets = conn.execute(text(query)).fetchall()

    if tickets:
        ticket_options = {f"#{t[0]} - {t[1]} [{t[2].upper()}]": t[0] for t in tickets}
        selected_ticket_str = st.radio("Select a Support Ticket to Inspect:", list(ticket_options.keys()))
        selected_ticket_id = ticket_options[selected_ticket_str]
    else:
        st.warning("No tickets found matching this status filter.")
        selected_ticket_id = None

    st.markdown("---")
    st.subheader("➕ Initiate a New Support Ticket")
    new_title = st.text_input("Short Ticket Title Summary:")
    new_user = st.text_input("Reporter Name/ID:")
    new_status = st.selectbox("Initial System Status:", ["open", "in_progress"])

    if st.button("Submit New Ticket"):
        # BONUS: Clean input validation and error messages
        if not new_title or not new_user:
            st.error("❌ Submission Blocked: Both Title and Reporter Name fields are mandatory.")
        else:
            with engine.connect() as conn:
                conn.execute(
                    text("INSERT INTO tickets (title, status, created_by) VALUES (:title, :status, :user)"),
                    {"title": new_title, "status": new_status, "user": new_user}
                )
                conn.commit()
            st.success("🏁 Ticket created successfully!")
            st.rerun()

with right_col:
    if selected_ticket_id:
        st.subheader(f"💬 Conversation Log for Ticket #{selected_ticket_id}")
        with engine.connect() as conn:
            messages = conn.execute(
                text(
                    "SELECT message_text, author, created_at FROM ticket_messages WHERE ticket_id = :id ORDER BY created_at ASC"),
                {"id": selected_ticket_id}
            ).fetchall()
            current_status = conn.execute(
                text("SELECT status FROM tickets WHERE ticket_id = :id"), {"id": selected_ticket_id}
            ).scalar()

        for msg in messages:
            st.markdown(f"**👤 {msg[1]}**")
            st.info(msg[0])

        st.markdown("---")
        st.subheader("✍️ Post an Internal Message Reply")
        reply_author = st.text_input("Author Name/ID:", key="reply_auth")
        reply_text = st.text_area("Message Body Text:", key="reply_txt")

        if st.button("Post Reply Message"):
            if not reply_author or not reply_text:
                st.error("❌ Message Blocked: Author and Reply text fields cannot be blank.")
            else:
                with engine.connect() as conn:
                    conn.execute(
                        text(
                            "INSERT INTO ticket_messages (ticket_id, message_text, author) VALUES (:t_id, :txt, :auth)"),
                        {"t_id": selected_ticket_id, "txt": reply_text, "auth": reply_author}
                    )
                    conn.commit()
                st.success("📨 Message posted!")
                st.rerun()

        st.markdown("---")
        st.subheader("⚙️ Modify Ticket Status")
        status_options = ["open", "in_progress", "resolved"]
        default_idx = status_options.index(current_status) if current_status in status_options else 0
        updated_status = st.selectbox("Change Status To:", status_options, index=default_idx)

        if st.button("Update System Status"):
            with engine.connect() as conn:
                conn.execute(
                    text("UPDATE tickets SET status = :status WHERE ticket_id = :id"),
                    {"status": updated_status, "id": selected_ticket_id}
                )
                conn.commit()
            st.success(f"⚡ Status altered to {updated_status.upper()}!")
            st.rerun()
