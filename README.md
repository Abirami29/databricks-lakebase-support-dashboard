# 🛠️ SyncMetrics Support Dashboard

A modern, feature-rich internal support ticketing system built with Streamlit and Databricks Lakebase (Postgres). This application provides a beautiful, intuitive interface for managing customer support tickets with real-time collaboration.

![Dashboard Overview](https://img.shields.io/badge/Status-Production_Ready-success)
![Platform](https://img.shields.io/badge/Platform-Databricks_Apps-blue)
![Database](https://img.shields.io/badge/Database-Lakebase_Postgres-purple)

## ✨ Features

### 📊 Dashboard Overview
* **Real-time Metrics**: Track total tickets, open, in-progress, and resolved counts
* **Visual Statistics**: Percentage breakdowns with color-coded indicators
* **Responsive Design**: Optimized for desktop and mobile viewing

### 🎫 Ticket Management
* **Create Tickets**: Simple form to create new support tickets
* **Status Filtering**: Filter tickets by status (Open, In Progress, Resolved)
* **Visual Status Badges**: Color-coded status indicators for quick identification
* **Input Validation**: Built-in validation with helpful error messages

### 💬 Conversation Threading
* **Message History**: View complete conversation timeline for each ticket
* **Timestamp Display**: See when each message was posted
* **Real-time Updates**: Automatic refresh after posting messages
* **Rich Formatting**: Beautiful message bubbles with author attribution

### ⚙️ Status Management
* **Workflow States**: Three-stage workflow (Open → In Progress → Resolved)
* **Visual Status Selector**: Dropdown with emoji indicators
* **Smart Validation**: Prevents redundant status updates
* **Instant Feedback**: Success animations on ticket actions

## 🏗️ Architecture

### Tech Stack
* **Frontend**: Streamlit with custom CSS
* **Backend**: Databricks Lakebase Postgres (autoscaling)
* **Database ORM**: SQLAlchemy
* **Secrets Management**: Databricks Secret Scope
* **Deployment**: Databricks Apps V2

### Database Schema

```sql
-- Tickets table
CREATE TABLE tickets (
    ticket_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'open',
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ticket messages table
CREATE TABLE ticket_messages (
    message_id SERIAL PRIMARY KEY,
    ticket_id INTEGER REFERENCES tickets(ticket_id),
    message_text TEXT NOT NULL,
    author VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 Getting Started

### Prerequisites

1. **Databricks Workspace** with Apps V2 enabled
2. **Lakebase Postgres Instance** (created and running)
3. **Databricks CLI** installed and configured
4. **Git repository** for version control

### Step 1: Set Up Lakebase Database

1. Create a Lakebase Postgres project and branch in your Databricks workspace
2. Note your connection details from the Lakebase UI:
   * Hostname (e.g., `ep-xxxxx.database.us-east-2.cloud.databricks.com`)
   * Port: `5432`
   * Database: `databricks_postgres`
   * User: Your email address
   * Password: Generated password

3. Create the database schema using the SQL commands above

### Step 2: Configure Databricks Secrets

Create a secret scope and add your Lakebase credentials:

```bash
# Create the secret scope (one-time setup)
databricks secrets create-scope lakebase-secrets

# Add the Lakebase hostname (JUST THE HOSTNAME, not the full URL)
databricks secrets put-secret lakebase-secrets lakebase-host \
  --string-value "ep-xxxxx.database.us-east-2.cloud.databricks.com"

# Add the Lakebase password
databricks secrets put-secret lakebase-secrets lakebase-password \
  --string-value "your-password-here"
```

**⚠️ IMPORTANT**: The `lakebase-host` secret must contain **ONLY the hostname**, not the full PostgreSQL URL!

✅ Correct:
```
ep-hidden-bread-d83qxt8s.database.us-east-2.cloud.databricks.com
```

❌ Wrong:
```
postgresql://user@host/db?sslmode=require
```

### Step 3: Configure app.yaml

The `app.yaml` file configures your Databricks App:

```yaml
command:
  - "sh"
  - "-c"
  - |
    pip install streamlit sqlalchemy psycopg2-binary databricks-sdk
    streamlit run app.py --server.port 8080

resources:
  - name: lakebase-host
    secret:
      scope: lakebase-secrets
      key: lakebase-host
  - name: lakebase-password
    secret:
      scope: lakebase-secrets
      key: lakebase-password

env:
  - name: LAKEBASE_PORT
    value: "5432"
  - name: LAKEBASE_DATABASE
    value: databricks_postgres
  - name: LAKEBASE_USER
    value: your-email@example.com  # Update with your email
```

**Update the `LAKEBASE_USER` with your actual email address!**

### Step 4: Deploy the App

1. **Commit your code to Git:**
   ```bash
   git add .
   git commit -m "Initial commit: SyncMetrics Support Dashboard"
   git push
   ```

2. **Deploy to Databricks:**
   ```bash
   databricks apps deploy ticketing-app
   ```

3. **Check deployment status:**
   ```bash
   databricks apps get ticketing-app
   ```

4. **View logs if needed:**
   ```bash
   databricks apps logs ticketing-app
   ```

## 📖 Usage Guide

### Creating a Ticket
1. Navigate to the **Create New Ticket** section in the left panel
2. Enter a ticket title (brief description of the issue)
3. Enter the reporter's name or ID
4. Select initial status (Open or In Progress)
5. Click **✨ Create Ticket**

### Viewing Tickets
1. Use the **Filter by Status** dropdown to narrow down tickets
2. Select a ticket from the radio button list
3. The conversation log appears in the right panel

### Adding Messages
1. Select a ticket from the left panel
2. Scroll to the **Add Message** section
3. Enter your name and message
4. Click **📤 Send Message**

### Updating Status
1. Select a ticket
2. Scroll to the **Update Status** section
3. Choose the new status from the dropdown
4. Click **🔄 Update Status**

## 🎨 Design Features

### Visual Design
* **Gradient Header**: Purple gradient with modern styling
* **Status Colors**: 
  * 🟢 Green for Open tickets
  * 🟡 Orange for In Progress
  * ⚫ Gray for Resolved
* **Message Bubbles**: Clean, readable conversation format
* **Hover Effects**: Interactive buttons with smooth transitions
* **Responsive Layout**: Two-column layout with proper spacing

### User Experience
* **Input Placeholders**: Helpful hints in all form fields
* **Validation Messages**: Clear error and success feedback
* **Empty States**: Helpful messages when no data is available
* **Tooltips**: Hover information on metrics
* **Celebration Animations**: Balloons on successful ticket creation

## 🔧 Troubleshooting

### Common Issues

#### 1. "Error reading app.yaml file"
* **Cause**: YAML syntax error or incorrect indentation
* **Solution**: Validate YAML format, ensure consistent spacing (2 spaces)

#### 2. Database Connection Failed
* **Cause**: Incorrect secret values or wrong hostname format
* **Solution**: 
  * Verify `lakebase-host` contains ONLY the hostname
  * Check that `lakebase-password` is correct
  * Ensure `LAKEBASE_USER` matches your Lakebase user

#### 3. Secret Not Found
* **Cause**: Secret scope or key doesn't exist
* **Solution**: Run the secret setup commands from Step 2

#### 4. App Won't Start
* **Cause**: Missing dependencies or wrong Python version
* **Solution**: Check logs with `databricks apps logs ticketing-app`

### Verifying Secrets

Run this code in a Databricks notebook to verify your secrets:

```python
from databricks.sdk import WorkspaceClient
import base64

client = WorkspaceClient()

# Check secrets exist
try:
    host_secret = client.secrets.get_secret(scope="lakebase-secrets", key="lakebase-host")
    pwd_secret = client.secrets.get_secret(scope="lakebase-secrets", key="lakebase-password")
    
    host = base64.b64decode(host_secret.value).decode('utf-8')
    password = base64.b64decode(pwd_secret.value).decode('utf-8')
    
    print(f"✅ Host secret: {host}")
    print(f"✅ Password secret: {'*' * len(password)}")
    
    # Verify hostname format
    if host.startswith("postgresql://"):
        print("❌ ERROR: lakebase-host contains a full URL, not just the hostname!")
    else:
        print("✅ Host format looks correct")
except Exception as e:
    print(f"❌ Error: {e}")
```

## 📁 Project Structure

```
databricks-lakebase-app-day-1-homework/
├── app.py                 # Main Streamlit application
├── app.yaml              # Databricks App configuration
├── README.md             # This file
├── setup_secrets.py      # Helper script for secret setup
├── requirements.txt      # Python dependencies
└── .gitignore           # Git ignore patterns
```

## 🔐 Security Best Practices

1. **Never commit secrets** to Git
2. **Use Databricks Secret Scope** for all sensitive data
3. **Rotate passwords** regularly
4. **Limit secret scope access** to authorized users only
5. **Use environment variables** for configuration

## 🚦 Development Workflow

1. **Make changes** to `app.py` locally
2. **Test locally** if possible (with connection to Lakebase)
3. **Commit to Git**
4. **Deploy** with `databricks apps deploy ticketing-app`
5. **Monitor logs** for any issues
6. **Test** the live app

## 📈 Future Enhancements

* [ ] User authentication and authorization
* [ ] Email notifications on ticket updates
* [ ] File attachments for tickets
* [ ] Advanced search and filtering
* [ ] Ticket assignment to team members
* [ ] SLA tracking and escalation
* [ ] Analytics and reporting dashboard
* [ ] Export tickets to CSV/PDF
* [ ] Dark mode toggle
* [ ] Mobile app version

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is for educational purposes as part of Databricks training.

## 👥 Authors

* Abi Attly - Built with ❤️ using Databricks Lakebase and Streamlit

## 🙏 Acknowledgments

* Databricks for the amazing Lakebase platform
* Streamlit for the intuitive UI framework
* The open-source community

---

**Need help?** Check the [troubleshooting section](#-troubleshooting) or review your Databricks workspace logs.