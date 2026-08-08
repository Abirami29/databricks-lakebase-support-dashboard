# Databricks Lakebase App - Day 1 Homework Submission

## Project Overview
This is a Streamlit-based ticket management application built on Databricks Lakebase, demonstrating real-time transactional data operations with low-latency responses.

---

## Deployment & Source Code

### Databricks App URL -- Note: This URL is only accessible when the Databricks workspace is running. If you are deploying a new instance, make sure your Databricks app is deployed and running and use the URL generated for you
https://ticketing-app-7474643870010414.aws.databricksapps.com/

---

## Application Screenshots

### Version 1 (Initial Implementation)


<img width="468" height="276" alt="image" src="https://github.com/user-attachments/assets/c3612527-ebc8-4e56-a4fc-7bec49a53cf1" />
<img width="468" height="266" alt="image" src="https://github.com/user-attachments/assets/65bd5eb2-db98-4cee-b5a4-16cb9dc3a86c" />

*Initial deployment of the SyncMetrics Internal Support Dashboard*

### Version 2 (Improved Visual Display)


<img width="468" height="276" alt="image" src="https://github.com/user-attachments/assets/1dcc5a7f-f9de-4bfd-8ce1-d35146e77167" />
<img width="468" height="256" alt="image" src="https://github.com/user-attachments/assets/5cd9c8e9-4f1e-449c-80d6-50bc3020a1db" />



*Enhanced visual design and user interface improvements*

---

## Database Schema

### Tables Created


<img width="468" height="239" alt="image" src="https://github.com/user-attachments/assets/25143cb2-b83e-48f7-a127-8166315ab52a" />
<img width="468" height="225" alt="image" src="https://github.com/user-attachments/assets/3f595e6c-4405-4854-a49a-248a75e0bc89" />


#### Tickets Table Data

<img width="468" height="210" alt="image" src="https://github.com/user-attachments/assets/116c6ea5-ae87-4928-95b4-fa469f1c9f01" />


#### Ticket Messages Table Data

<img width="468" height="187" alt="image" src="https://github.com/user-attachments/assets/5af1db64-93e6-4a21-836e-b93a4a1cb795" />


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
