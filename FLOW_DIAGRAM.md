# 🛠️ SyncMetrics Support Dashboard - Flow Diagram

## System Architecture Overview

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃           🎨 USER INTERFACE (Streamlit Web App)           ┃
┃  ┌─────────────────────────────────────────────────────┐ ┃
┃  │  📊 Dashboard Metrics │ 📋 Left Panel │ 💬 Right    │ ┃
┃  │  Real-time Stats      │ Ticket List   │ Ticket      │ ┃
┃  │  (4 metric cards)     │ & Creation    │ Details     │ ┃
┃  └─────────────────────────────────────────────────────┘ ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                            ▲
                            │ Streamlit Events
                            │ (User clicks, forms)
                            ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃      🐍 APPLICATION LOGIC (Python in app.py)             ┃
┃  ✓ Input validation      ✓ State management              ┃
┃  ✓ Query building        ✓ Error handling                ┃
┃  ✓ Data transformation   ✓ UI rendering                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                            ▲
                            │ SQLAlchemy ORM
                            │ (Query execution)
                            ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃      🔐 DATABRICKS SECRETS API (Secret Scope Mgmt)       ┃
┃  • Scope: lakebase-secrets                               ┃
┃  • Key 1: lakebase-host (connection URL)                 ┃
┃  • Key 2: lakebase-password (base64 encoded)             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                            ▲
                            │ Base64 decode
                            │ & authenticate
                            ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    💾 DATABRICKS LAKEBASE (PostgreSQL-Compatible DB)     ┃
┃  ┌────────────────────┐  ┌──────────────────────────┐  ┃
┃  │  📌 TICKETS TABLE  │  │ 💬 TICKET_MESSAGES TABLE │  ┃
┃  ├────────────────────┤  ├──────────────────────────┤  ┃
┃  │ • ticket_id (PK)   │  │ • message_id (PK)        │  ┃
┃  │ • title            │  │ • ticket_id (FK)         │  ┃
┃  │ • status           │  │ • message_text           │  ┃
┃  │ • created_by       │  │ • author                 │  ┃
┃  │ • created_at       │  │ • created_at             │  ┃
┃  └────────────────────┘  └──────────────────────────┘  ┃
┃                                                         ┃
┃  📊 Row-based storage optimized for OLTP               ┃
┃  🔒 ACID compliance & concurrent access                ┃
┃  ⚡ Low-latency reads/writes                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## User Flow Diagrams

### 1. Application Initialization Flow

```
START
  │
  ├─► Load Environment
  │    ├─ Read app.py configuration
  │    ├─ Load Streamlit settings
  │    └─ Initialize logging
  │
  ├─► Access Secrets
  │    ├─ WorkspaceClient() → Databricks SDK
  │    ├─ get_secret("lakebase-secrets", "lakebase-host")
  │    ├─ Base64 decode connection URL
  │    └─ Return database URL
  │
  ├─► Establish Database Connection
  │    ├─ create_engine(DATABASE_URL)
  │    ├─ Initialize SQLAlchemy ORM
  │    └─ Test connection
  │
  └─► Render Dashboard
       └─ Display UI components
```

---

### 2. Dashboard Overview (Metrics) Flow

```
USER LOADS PAGE
  │
  ├─► Execute Aggregate Queries
  │    │
  │    ├─► Query 1: SELECT COUNT(*) FROM tickets
  │    │    └─ Result: total_t (all tickets)
  │    │
  │    ├─► Query 2: SELECT COUNT(*) FROM tickets WHERE status='open'
  │    │    └─ Result: open_t (new tickets)
  │    │
  │    ├─► Query 3: SELECT COUNT(*) FROM tickets WHERE status='in_progress'
  │    │    └─ Result: prog_t (tickets being worked on)
  │    │
  │    └─► Query 4: SELECT COUNT(*) FROM tickets WHERE status='resolved'
  │         └─ Result: resolved_t (completed tickets)
  │
  ├─► Calculate Percentages
  │    ├─ Open %    = (open_t / total_t) * 100
  │    ├─ Progress % = (prog_t / total_t) * 100
  │    └─ Resolved % = (resolved_t / total_t) * 100
  │
  └─► Render 4 Metric Cards
       ├─ 🏛️  Total Tickets
       ├─ 🟢 Open
       ├─ 🟡 In Progress
       └─ ✅ Resolved
```

---

### 3. Ticket Filtering & Selection Flow

```
USER SELECTS STATUS FILTER
  │
  ├─► Dropdown Options: ["All", "open", "in_progress", "resolved"]
  │
  ├─► Build SQL Query
  │    ├─ If "All": SELECT * FROM tickets
  │    └─ Else: SELECT * FROM tickets WHERE status = '{filter}'
  │
  ├─► Execute Query
  │    ├─ Fetch all matching rows
  │    └─ Convert to ticket list
  │
  ├─► Check Results
  │    │
  │    ├─ IF tickets found:
  │    │   │
  │    │   ├─► Format Display
  │    │   │    └─ Create list: ["🎫 #1 - Title", "🎫 #2 - Title", ...]
  │    │   │
  │    │   ├─► Show Radio Button Selection
  │    │   │    └─ User selects one ticket
  │    │   │
  │    │   └─► Display Status Badge
  │    │        └─ Color-coded status indicator
  │    │
  │    └─ ELSE:
  │        └─ Show: "🔍 No tickets found matching this status filter."
  │
  └─► selected_ticket_id = (user's selection)
```

---

### 4. Create New Ticket Flow

```
USER FILLS TICKET FORM
  │
  ├─► Input Fields
  │    ├─ new_title = text_input("📝 Ticket Title")
  │    ├─ new_user = text_input("👤 Reporter")
  │    └─ new_status = selectbox("🟢 Initial Status")
  │
  ├─► User Clicks "✨ Create Ticket"
  │
  ├─► VALIDATION
  │    │
  │    ├─ IF (new_title == "") OR (new_user == ""):
  │    │   │
  │    │   └─► Show Error: "❌ Please fill in all required fields"
  │    │       └─ STOP / Return to form
  │    │
  │    └─ ELSE: Proceed to database insert
  │
  ├─► Database Insert
  │    │
  │    ├─► SQL: INSERT INTO tickets (title, status, created_by)
  │    │        VALUES (:title, :status, :user)
  │    │
  │    ├─► Parameters:
  │    │    ├─ title = new_title
  │    │    ├─ status = new_status
  │    │    └─ user = new_user
  │    │
  │    ├─► Commit Transaction
  │    │    └─ Data persisted to Lakebase
  │    │
  │    └─► Row inserted with:
  │         ├─ ticket_id (auto-generated)
  │         └─ created_at (CURRENT_TIMESTAMP)
  │
  ├─► Show Success
  │    ├─ ✅ "Ticket has been created and added to the system."
  │    ├─ 🎉 Balloons animation
  │    └─ st.rerun() → Refresh page
  │
  └─► END (Page reloads with new ticket visible)
```

---

### 5. View Ticket Conversation Flow

```
USER SELECTS A TICKET
  │
  ├─► selected_ticket_id is set
  │
  ├─► Right Panel Activates
  │
  ├─► Fetch Message History
  │    │
  │    ├─► SQL Query:
  │    │    SELECT message_text, author, created_at
  │    │    FROM ticket_messages
  │    │    WHERE ticket_id = :id
  │    │    ORDER BY created_at ASC
  │    │
  │    ├─► Get Current Status:
  │    │    SELECT status FROM tickets WHERE ticket_id = :id
  │    │
  │    └─► Fetch current_status variable
  │
  ├─► Display Messages
  │    │
  │    ├─ IF messages exist:
  │    │   │
  │    │   ├─► FOR EACH message:
  │    │   │    ├─ Render message bubble
  │    │   │    ├─ Show: 👤 Author name
  │    │   │    ├─ Show: · Timestamp (formatted)
  │    │   │    └─ Show: Message content
  │    │   │
  │    │   └─ Messages sorted by created_at (oldest first)
  │    │
  │    └─ ELSE:
  │        └─ Show: "📢 No messages yet. Be the first to comment!"
  │
  └─► Display Message Section Headers
       ├─ 💬 Conversation Log - Ticket #<id>
       └─ Ready for user input
```

---

### 6. Add Message to Ticket Flow

```
USER ADDS A MESSAGE
  │
  ├─► Input Fields
  │    ├─ reply_author = text_input("👤 Your Name")
  │    └─ reply_text = text_area("📝 Message")
  │
  ├─► User Clicks "📤 Send Message"
  │
  ├─► VALIDATION
  │    │
  │    ├─ IF (reply_author == "") OR (reply_text == ""):
  │    │   │
  │    │   └─► Show Error: "❌ Please provide both name and message"
  │    │       └─ STOP / Return to form
  │    │
  │    └─ ELSE: Proceed to insert
  │
  ├─► Database Insert
  │    │
  │    ├─► SQL: INSERT INTO ticket_messages
  │    │        (ticket_id, message_text, author)
  │    │        VALUES (:t_id, :txt, :auth)
  │    │
  │    ├─► Parameters:
  │    │    ├─ t_id = selected_ticket_id
  │    │    ├─ txt = reply_text
  │    │    └─ auth = reply_author
  │    │
  │    ├─► Commit Transaction
  │    │
  │    └─► Row inserted with:
  │         ├─ message_id (auto-generated)
  │         ├─ ticket_id (foreign key reference)
  │         └─ created_at (CURRENT_TIMESTAMP)
  │
  ├─► Show Success
  │    ├─ ✅ "Message posted successfully!"
  │    └─ st.rerun() → Refresh page
  │
  └─► END (Conversation log updated with new message)
```

---

### 7. Update Ticket Status Flow

```
USER CHANGES TICKET STATUS
  │
  ├─► Get Current Status
  │    └─ current_status (fetched earlier)
  │
  ├─► Status Options
  │    ├─ 🟢 Open
  │    ├─ 🟡 In Progress
  │    └─ ✅ Resolved
  │
  ├─► User Selects New Status
  │    └─ updated_status = st.selectbox(...)
  │
  ├─► User Clicks "🔄 Update Status"
  │
  ├─► Status Change Check
  │    │
  │    ├─ IF updated_status == current_status:
  │    │   │
  │    │   └─► Show Info: "💡 Status already set to <status>"
  │    │       └─ STOP / No update needed
  │    │
  │    └─ ELSE: Proceed to update
  │
  ├─► Database Update
  │    │
  │    ├─► SQL: UPDATE tickets
  │    │        SET status = :status
  │    │        WHERE ticket_id = :id
  │    │
  │    ├─► Parameters:
  │    │    ├─ status = updated_status
  │    │    └─ id = selected_ticket_id
  │    │
  │    ├─► Commit Transaction
  │    │    └─ Data persisted to Lakebase
  │    │
  │    └─ Status column updated
  │
  ├─► Show Success
  │    ├─ ✅ "Status updated to <NEW_STATUS>"
  │    └─ st.rerun() → Refresh page
  │
  └─► END (Metrics and ticket list updated to reflect status change)
```

---

## Data Flow: From UI to Database

```
┌──────────────────────┐
│   USER ACTION        │
│  (Create/Update)     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│   INPUT VALIDATION                           │
│  • Check required fields                     │
│  • Validate format                           │
│  • Prevent empty submissions                 │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│   SQL QUERY BUILDING                         │
│  • Construct SQL statement                   │
│  • Parameterize values                       │
│  • Prevent SQL injection                     │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│   SQLAlchemy ORM EXECUTION                   │
│  • Build connection                          │
│  • Execute query                             │
│  • Handle transaction                        │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│   POSTGRES (Lakebase) CONNECTION             │
│  • Authenticate with credentials             │
│  • Execute SQL on remote database            │
│  • Return results (if applicable)            │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│   TRANSACTION COMMIT                         │
│  • Write data to disk                        │
│  • Update indices                            │
│  • Release locks                             │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│   RESPONSE TO FRONTEND                       │
│  • Show success/error message                │
│  • Trigger page reload (st.rerun)            │
│  • Refresh metrics and lists                 │
└──────────────────────────────────────────────┘
```

---

## State Management Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   STREAMLIT PAGE LOAD                       │
│                                                             │
│  1. ✅ Sidebar Initialization                             │
│     └─ App loads in "wide" layout                          │
│                                                             │
│  2. ✅ CSS & Styling Applied                              │
│     └─ Custom HTML/CSS injected via st.markdown()          │
│                                                             │
│  3. ✅ Database Connection Established                    │
│     └─ engine = create_engine(DATABASE_URL)                │
│                                                             │
│  4. ✅ Fetch All Metrics                                  │
│     ├─ total_t, open_t, prog_t, resolved_t                │
│     └─ Display in 4 metric columns                         │
│                                                             │
│  5. ✅ Render Left Panel (Ticket Management)              │
│     ├─ Status filter dropdown                              │
│     ├─ Ticket selection radio                              │
│     ├─ Create ticket form                                  │
│     └─ Status badge display                                │
│                                                             │
│  6. ✅ Render Right Panel (Ticket Details)                │
│     ├─ IF ticket selected:                                 │
│     │   ├─ Display conversation log                        │
│     │   ├─ Add message form                                │
│     │   └─ Update status section                           │
│     └─ ELSE:                                               │
│         └─ "Select a ticket" prompt                        │
│                                                             │
│  7. ✅ Listen for User Events                             │
│     ├─ Form submissions                                    │
│     ├─ Button clicks                                       │
│     └─ Dropdown selections                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Database Query Summary

### Read Operations (SELECT)

```
1. Load Dashboard Metrics
   ├─ SELECT COUNT(*) FROM tickets
   ├─ SELECT COUNT(*) FROM tickets WHERE status='open'
   ├─ SELECT COUNT(*) FROM tickets WHERE status='in_progress'
   └─ SELECT COUNT(*) FROM tickets WHERE status='resolved'

2. Filter Tickets by Status
   └─ SELECT * FROM tickets [WHERE status = '{filter}']

3. Load Ticket Conversation
   └─ SELECT message_text, author, created_at
      FROM ticket_messages
      WHERE ticket_id = :id
      ORDER BY created_at ASC

4. Get Current Ticket Status
   └─ SELECT status FROM tickets WHERE ticket_id = :id
```

### Write Operations (INSERT/UPDATE)

```
1. Create New Ticket
   └─ INSERT INTO tickets (title, status, created_by)
      VALUES (:title, :status, :user)

2. Add Message to Ticket
   └─ INSERT INTO ticket_messages (ticket_id, message_text, author)
      VALUES (:t_id, :txt, :auth)

3. Update Ticket Status
   └─ UPDATE tickets SET status = :status WHERE ticket_id = :id
```

---

## Error Handling Flow

```
┌─────────────────────────────────────────┐
│         USER ACTION                     │
└──────────┬──────────────────────────────┘
           │
           ▼
    ┌─────────────────────────────────┐
    │  VALIDATION CHECK               │
    │  • Empty fields?                │
    │  • Duplicate status?            │
    └─────────┬───────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
    ▼                   ▼
ERROR                SUCCESS
  │                     │
  │                     ├─► Execute SQL
  │                     ├─► Commit Transaction
  │                     ├─► Show Success Message
  │                     └─► Reload Page
  │
  └─► Show Error Alert
      └─ st.error() with description
```

---

## Technology Stack & Data Flow

```
Frontend Layer:
┌─────────────────────────────┐
│ Streamlit UI                │
│ • Widgets (forms, buttons)  │
│ • Custom CSS styling        │
│ • Real-time responsiveness  │
└────────────┬────────────────┘
             │
Application Layer:
┌────────────────────────────────────────┐
│ Python Logic (app.py)                  │
│ • Input validation                     │
│ • Session state management             │
│ • Error handling                       │
│ • User feedback                        │
└────────────┬─────────────────────────────┘
             │
ORM Layer:
┌────────────────────────────────────────┐
│ SQLAlchemy                             │
│ • Query building                       │
│ • Parameter binding                    │
│ • Connection pooling                   │
│ • Transaction management               │
└────────────┬─────────────────────────────┘
             │
Database Layer:
┌────────────────────────────────────────┐
│ Databricks Lakebase (PostgreSQL)       │
│ • ACID transactions                    │
│ • Relational data model                │
│ • Concurrent access                    │
│ • Data persistence                     │
└────────────────────────────────────────┘
```

---

## Performance Characteristics

### Query Latency Profile

```
Operation                          Typical Latency
─────────────────────────────────────────────────
Dashboard Load (4 COUNT queries)   ~100-200ms
Fetch ticket list (SELECT *)       ~50-150ms
Load conversation (SELECT msgs)    ~50-100ms
Create ticket (INSERT)             ~100-200ms
Add message (INSERT)               ~100-150ms
Update status (UPDATE)             ~50-100ms
```

### Lakebase Advantages for This Use Case

```
✅ Low-latency reads        → Fast ticket list loading
✅ Concurrent writes        → Multiple users updating simultaneously
✅ ACID guarantees          → Data consistency
✅ Row-based storage        → Optimized for point queries
✅ Transactional support    → Safe status updates
```

---

## Deployment Flow

```
Developer
    │
    ├─► Git Commit & Push
    │
    ├─► databricks apps deploy ticketing-app
    │
    ├─► Deploy reads app.yaml config
    │    ├─ Install dependencies (pip install ...)
    │    ├─ Start Streamlit server (port 8080)
    │    ├─ Load secrets (lakebase-host, lakebase-password)
    │    └─ Connect to Lakebase database
    │
    ├─► Monitor Deployment
    │    └─ databricks apps logs ticketing-app
    │
    └─► App Running
         └─ Accessible via Databricks Apps URL
```

---

## Summary: Request-Response Cycle

```
1️⃣  USER INTERACTION
    └─ Click button / submit form / select option

2️⃣  STREAMLIT DETECTION
    └─ Captures event

3️⃣  VALIDATION
    └─ Check input constraints

4️⃣  SQL GENERATION
    └─ Build parameterized query

5️⃣  DATABASE CALL
    └─ Send query to Lakebase via SQLAlchemy

6️⃣  LAKEBASE PROCESSING
    └─ Execute & persist changes

7️⃣  RESPONSE HANDLING
    └─ Commit transaction / return results

8️⃣  FEEDBACK
    └─ Show success/error to user

9️⃣  REFRESH
    └─ Reload page (st.rerun()) to show updates

🔟 DISPLAY
    └─ User sees fresh data
```

---

*Last Updated: August 8, 2026*  
*SyncMetrics Support Dashboard v1.0*
