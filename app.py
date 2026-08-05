import base64
import streamlit as st
from sqlalchemy import create_engine, text
from databricks.sdk import WorkspaceClient

st.set_page_config(
    page_title="SyncMetrics Support Core",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better visual design
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
    }
    
    /* Status badges */
    .status-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 0.5rem;
    }
    
    .status-open {
        background-color: #10b981;
        color: white;
    }
    
    .status-in_progress {
        background-color: #f59e0b;
        color: white;
    }
    
    .status-resolved {
        background-color: #6b7280;
        color: white;
    }
    
    /* Card styling */
    .ticket-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Message bubbles */
    .message-bubble {
        background: #f3f4f6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.75rem;
        border-left: 3px solid #667eea;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Section headers */
    .section-header {
        color: #1f2937;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

_w = WorkspaceClient()
_SCOPE = "lakebase-secrets"
_KEY = "lakebase-host"

def _lakebase_url() -> str:
    """Fetch and decode the Lakebase connection URL from the Databricks secret scope."""
    secret = _w.secrets.get_secret(scope=_SCOPE, key=_KEY)
    return base64.b64decode(secret.value).decode("utf-8")

DATABASE_URL = _lakebase_url()
engine = create_engine(DATABASE_URL)

# Main header with gradient
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 2.5rem;">🛠️ SyncMetrics Internal Support Dashboard</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Manage and track customer support tickets</p>
</div>
""", unsafe_allow_html=True)

# BONUS: Ticket statistics summary cards with improved visuals
st.markdown('<p class="section-header">📊 Dashboard Overview</p>', unsafe_allow_html=True)

with engine.connect() as conn:
    total_t = conn.execute(text("SELECT COUNT(*) FROM tickets")).scalar()
    open_t = conn.execute(text("SELECT COUNT(*) FROM tickets WHERE status='open'")).scalar()
    prog_t = conn.execute(text("SELECT COUNT(*) FROM tickets WHERE status='in_progress'")).scalar()
    resolved_t = conn.execute(text("SELECT COUNT(*) FROM tickets WHERE status='resolved'")).scalar()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        label="🏛️ Total Tickets",
        value=total_t,
        help="Total number of tickets in the system"
    )
with col2:
    st.metric(
        label="🟢 Open",
        value=open_t,
        delta=f"{int(open_t/total_t*100) if total_t > 0 else 0}%",
        help="New tickets awaiting response"
    )
with col3:
    st.metric(
        label="🟡 In Progress",
        value=prog_t,
        delta=f"{int(prog_t/total_t*100) if total_t > 0 else 0}%",
        help="Tickets currently being worked on"
    )
with col4:
    st.metric(
        label="✅ Resolved",
        value=resolved_t,
        delta=f"{int(resolved_t/total_t*100) if total_t > 0 else 0}%",
        help="Successfully resolved tickets"
    )

st.markdown("<br>", unsafe_allow_html=True)

left_col, right_col = st.columns(2)

with left_col:
    st.markdown('<p class="section-header">📋 Active System Tickets</p>', unsafe_allow_html=True)
    # BONUS: Filtering capabilities by ticket status
    status_filter = st.selectbox(
        "🔍 Filter by Status",
        ["All", "open", "in_progress", "resolved"],
        help="Filter tickets by their current status"
    )

    query = "SELECT * FROM tickets"
    if status_filter != "All":
        query += f" WHERE status = '{status_filter}'"

    with engine.connect() as conn:
        tickets = conn.execute(text(query)).fetchall()

    if tickets:
        # Create visually enhanced ticket options with status badges
        ticket_display = []
        ticket_map = {}
        for t in tickets:
            status_class = f"status-{t[2]}"
            display = f"🎫 #{t[0]} - {t[1]}"
            ticket_display.append(display)
            ticket_map[display] = (t[0], t[2])
        
        selected_ticket_str = st.radio(
            "Select a Support Ticket:",
            ticket_display,
            format_func=lambda x: x
        )
        selected_ticket_id = ticket_map[selected_ticket_str][0]
        selected_status = ticket_map[selected_ticket_str][1]
        
        # Show status badge for selected ticket
        status_color_map = {
            "open": "#10b981",
            "in_progress": "#f59e0b",
            "resolved": "#6b7280"
        }
        st.markdown(
            f'<span style="background-color: {status_color_map.get(selected_status, "#6b7280")}; '
            f'color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600;"'
            f'>{selected_status.upper().replace("_", " ")}</span>',
            unsafe_allow_html=True
        )
    else:
        st.warning("🔍 No tickets found matching this status filter.")
        selected_ticket_id = None

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<p class="section-header">➕ Create New Ticket</p>', unsafe_allow_html=True)
    
    new_title = st.text_input("📝 Ticket Title", placeholder="Brief description of the issue...")
    new_user = st.text_input("👤 Reporter", placeholder="Name or user ID...")
    new_status = st.selectbox("🟢 Initial Status", ["open", "in_progress"])

    if st.button("✨ Create Ticket", use_container_width=True):
        # BONUS: Clean input validation and error messages
        if not new_title or not new_user:
            st.error("❌ **Error**: Please fill in all required fields (Title and Reporter).")
        else:
            with engine.connect() as conn:
                conn.execute(
                    text("INSERT INTO tickets (title, status, created_by) VALUES (:title, :status, :user)"),
                    {"title": new_title, "status": new_status, "user": new_user}
                )
                conn.commit()
            st.success("✅ **Success!** Ticket has been created and added to the system.")
            st.balloons()
            st.rerun()

with right_col:
    if selected_ticket_id:
        st.markdown(f'<p class="section-header">💬 Conversation Log - Ticket #{selected_ticket_id}</p>', unsafe_allow_html=True)
        
        with engine.connect() as conn:
            messages = conn.execute(
                text(
                    "SELECT message_text, author, created_at FROM ticket_messages WHERE ticket_id = :id ORDER BY created_at ASC"),
                {"id": selected_ticket_id}
            ).fetchall()
            current_status = conn.execute(
                text("SELECT status FROM tickets WHERE ticket_id = :id"), {"id": selected_ticket_id}
            ).scalar()

        if messages:
            for msg in messages:
                # Format timestamp if available
                timestamp = msg[2].strftime("%b %d, %Y at %I:%M %p") if msg[2] else "Unknown time"
                st.markdown(
                    f'<div class="message-bubble">'
                    f'<strong style="color: #667eea;">👤 {msg[1]}</strong> '
                    f'<span style="color: #9ca3af; font-size: 0.85rem;">· {timestamp}</span><br>'
                    f'<span style="color: #374151;">{msg[0]}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.info("📢 No messages yet. Be the first to comment!")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="section-header">✍️ Add Message</p>', unsafe_allow_html=True)
        
        reply_author = st.text_input("👤 Your Name", key="reply_auth", placeholder="Enter your name...")
        reply_text = st.text_area(
            "📝 Message",
            key="reply_txt",
            placeholder="Type your message here...",
            height=120
        )

        if st.button("📤 Send Message", use_container_width=True):
            if not reply_author or not reply_text:
                st.error("❌ **Error**: Please provide both your name and a message.")
            else:
                with engine.connect() as conn:
                    conn.execute(
                        text(
                            "INSERT INTO ticket_messages (ticket_id, message_text, author) VALUES (:t_id, :txt, :auth)"),
                        {"t_id": selected_ticket_id, "txt": reply_text, "auth": reply_author}
                    )
                    conn.commit()
                st.success("✅ **Message posted successfully!**")
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="section-header">⚙️ Update Status</p>', unsafe_allow_html=True)
        
        status_options = ["open", "in_progress", "resolved"]
        status_labels = {
            "open": "🟢 Open",
            "in_progress": "🟡 In Progress",
            "resolved": "✅ Resolved"
        }
        default_idx = status_options.index(current_status) if current_status in status_options else 0
        
        updated_status = st.selectbox(
            "Change ticket status to:",
            status_options,
            index=default_idx,
            format_func=lambda x: status_labels.get(x, x)
        )

        if st.button("🔄 Update Status", use_container_width=True):
            if updated_status == current_status:
                st.info("💡 Status is already set to **{}**." .format(updated_status.upper().replace("_", " ")))
            else:
                with engine.connect() as conn:
                    conn.execute(
                        text("UPDATE tickets SET status = :status WHERE ticket_id = :id"),
                        {"status": updated_status, "id": selected_ticket_id}
                    )
                    conn.commit()
                st.success(f"✅ **Status updated** to **{updated_status.upper().replace('_', ' ')}**!")
                st.rerun()
    else:
        # Empty state when no ticket is selected
        st.markdown(
            '<div style="text-align: center; padding: 3rem 1rem; color: #9ca3af;">'
            '<h3 style="color: #6b7280;">👈 Select a ticket</h3>'
            '<p>Choose a ticket from the left panel to view its conversation and details.</p>'
            '</div>',
            unsafe_allow_html=True
        )
