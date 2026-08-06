# Databricks Lakebase App - Day 1 Homework Submission

## Project Overview
This is a Streamlit-based ticket management application built on Databricks Lakebase, demonstrating real-time transactional data operations with low-latency responses.

---

## Deployment & Source Code

### Databricks App URL
https://ticketing-app-7474643870010414.aws.databricksapps.com/

### Source Code Repository
https://github.com/Abirami29/databricks-lakebase-app-day-1-homework.git

---

## Application Screenshots

### Version 1 (Initial Implementation)
![V1 Screenshot](./screenshots/v1-initial.png)
*Initial deployment of the SyncMetrics Internal Support Dashboard*

### Version 2 (Improved Visual Display)
![V2 Screenshot - Part 1](./screenshots/v2-improved-1.png)
![V2 Screenshot - Part 2](./screenshots/v2-improved-2.png)
*Enhanced visual design and user interface improvements*

---

## Database Schema

### Tables Created
![Tables Overview](./screenshots/tables-overview.png)

#### Tickets Table
![Tickets Table](./screenshots/table-tickets.png)

#### Ticket Messages Table
![Ticket Messages Table](./screenshots/table-messages.png)

---

## Reflection & Learning

### Q1: What was the most difficult part?

**Answer:**
Vibe coding and troubleshooting with Genie proved challenging. The AI kept going into loops, undoing and redoing the same changes repeatedly. This required manual debugging and troubleshooting to break the cycle.

Additionally, unfamiliarity with the Databricks platform made it difficult to locate features and understand how different components interact. However, this was a great learning opportunity that improved my understanding of the platform.

### Q2: How is Lakebase different from storing this data in a traditional analytics table?

**Answer:**
Lakebase tables are fundamentally different from traditional analytics tables in several key ways:

- **Concurrency Model**: Lakebase tables include referential indexes and are designed to handle high-frequency concurrent read-writes, similar to OLTP (Online Transaction Processing) databases.

- **Storage Format**: 
  - Lakebase uses **row-based storage** optimized for fast point lookups and transactional operations
  - Traditional analytics tables use **columnar storage** optimized for heavy scanning and aggregations

- **Latency Profile**: Lakebase delivers low-latency responses for individual row operations and point queries, making it ideal for real-time applications like ticket management systems.

- **Use Cases**:
  - Lakebase: Real-time ticket updates, concurrent user interactions, transactional consistency
  - Analytics Tables: Batch processing, complex aggregations, historical analysis

### Q3: What feature would you add next?

**Answer:**
The next milestone feature would be integrating an **asynchronous Spark processing script** that:

1. Queries vector search endpoints inside **Databricks Mosaic AI**
2. Allows an autonomous AI agent to read ticket histories and context
3. Auto-generates intelligent customer responses based on ticket content and history
4. Provides real-time suggestions to support staff for faster resolution

This would leverage Lakebase's low-latency reads to power AI-driven automation, significantly improving ticket resolution times and customer satisfaction.

---

## Key Technologies Used

- **Streamlit**: Frontend framework for rapid dashboard development
- **Databricks Lakebase**: Transactional database layer for real-time data operations
- **SQLAlchemy**: ORM for database interactions
- **Python 3.11**: Core application language
- **PostgreSQL-compatible API**: For Lakebase connectivity

---

## Features Implemented

✅ Real-time ticket statistics dashboard  
✅ Ticket filtering by status (open, in_progress, resolved)  
✅ Create new support tickets  
✅ View ticket conversation history  
✅ Post replies to tickets  
✅ Update ticket status  
✅ Input validation and error handling  
✅ Secure secret management via Databricks Secrets API  

---

## Challenges Overcome

1. **Connection Issues**: Successfully debugged and resolved PostgreSQL connection string configuration using base64-encoded secrets
2. **AI Assistant Loops**: Manually intervened to stop repetitive changes and take direct control of fixes
3. **Platform Learning Curve**: Navigated Databricks UI and learned proper credential management
4. **Concurrent Writes**: Ensured proper transaction handling for simultaneous ticket updates

---

*Last Updated: August 6, 2026*
