Markdown
# 🏎️ Formula 1 End-to-End Data Engineering Pipeline

A production-ready ETL pipeline that ingests 70+ years of Formula 1 history, loads it into a **Cloud Serverless PostgreSQL (Neon)**, performs advanced optimizations (Materialized Views), and visualizes insights via Streamlit.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Serverless_Neon-elephant)
![uv](https://img.shields.io/badge/uv-Package_Manager-purple)
![Streamlit](https://img.shields.io/badge/Deployment-Streamlit_Cloud-FF4B4B)

---

## 📌 Project Overview
This project demonstrates a full-cycle, modern Data Engineering workflow:
1.  **Ingestion:** Extracting data from 14 raw CSV files (~1M rows).
2.  **Processing (Fault-Tolerant):** Cleaning and transforming data using Pandas. The pipeline features **Chunking** and **Exponential Backoff Retries** to survive network glitches during cloud uploads.
3.  **Storage:** Loading data into a normalized, Cloud-based PostgreSQL schema (Neon).
4.  **Optimization:** Implementing **Materialized Views** and **Clustered Indexes** to reduce complex JOIN query times by **94%**.
5.  **Automation:** Database Triggers and refresh functions for state management.
6.  **Visualization:** Interactive, public-facing dashboard for analyzing driver and constructor performance.

## 📂 Repository Structure
```text
formula1/
│
├── data/                  # Source CSV files (circuits, races, lap_times, etc.)
├── docs/                  # In-depth architectural documentation
├── sql/                   # Advanced SQL Architecture
│   ├── analysis/          # Analytical queries & Master Views
│   ├── automation/        # Triggers and Functions
│   └── optimization/      # Indexing and Materialization scripts
│
├── src/                   
│   ├── etl_pipeline.py    # Main ETL logic (Pandas + SQLAlchemy + Retries)
│   ├── app.py             # Streamlit Dashboard application
│   └── reset_pipeline.py  # Teardown & Idempotency script
│
├── .env                   # Environment variables (Ignored in Git)
├── requirements.txt       # Exported dependencies for Streamlit Cloud
├── pyproject.toml         # uv project configuration
└── uv.lock                # uv dependency lockfile

🛠️ Tech Stack & Key Features
Modern Dependency Management: Migrated from standard pip to uv for lightning-fast, deterministic virtual environments.

Serverless Infrastructure: Transitioned from local Docker-Compose to Neon.tech Serverless PostgreSQL for zero-maintenance cloud hosting.

Idempotency: Pipeline uses TRUNCATE ... CASCADE and a dedicated reset_pipeline.py to ensure "Clean Slate" runs without Zombie Data.

Security: Strict separation of secrets using python-dotenv.

🚀 How to Run Locally
1. Setup the Environment
This project uses uv for dependency management.

Bash
# Install dependencies
uv sync
2. Configure Secrets
Create a .env file in the root directory and add your database connection string:

קטע קוד
DATABASE_URL="postgresql://user:password@your-neon-host.aws.neon.tech/dbname?sslmode=require"
3. Run the ETL Pipeline

Bash
uv run src/etl_pipeline.py
4. Launch the Dashboard

Bash
uv run streamlit run src/app.py
📚 Documentation & Deep Dives
For a detailed breakdown of the engineering decisions, check the docs/ folder:

📄 [Level 1] Schema Design: How we modeled the Relational Database.

📄 [Level 2] Python ETL Architecture: Fault tolerance and chunking strategies.

📄 [Level 3] Analytical Queries: Business insights extracted from the data.

📄 [Level 4] Database Optimization: Indexing strategies and Clustered Indexes.

📄 [Level 5] Materialized Views: Benchmarking performance (94% speedup).

👨‍💻 Author: Dvir - Data Engineering Student

Built as a comprehensive Capstone Project demonstrating end-to-end Data Engineering capabilities.