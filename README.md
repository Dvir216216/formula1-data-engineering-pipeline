Markdown

# 🏎️ Formula 1 End-to-End Data Engineering Pipeline

A production-ready, containerized ETL pipeline that ingests 70+ years of Formula 1 history, loads it into PostgreSQL, performs advanced optimizations (Materialized Views), and visualizes insights via Streamlit.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-elephant)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B)

---

## 📌 Project Overview
This project demonstrates a full-cycle Data Engineering workflow:
1.  **Ingestion:** Extracting data from 14 raw CSV files.
2.  **Processing:** Cleaning, transforming, and validating data using Pandas.
3.  **Storage:** Loading data into a normalized PostgreSQL schema.
4.  **Optimization:** Implementing **Materialized Views** and **Clustered Indexes** to reduce query time by **94%**.
5.  **Visualization:** Interactive dashboard for analyzing driver and constructor performance.

## 📂 Repository Structure
```text
formula1-pipeline/
│
├── data/                  # Source CSV files (circuits.csv, races.csv, etc.)
├── src/
│   ├── etl_pipeline.py    # Main ETL logic (Pandas + SQLAlchemy)
│   ├── dashboard.py       # Streamlit application code
├── docs/                  # Detailed documentation (Level 1-6)
├── sql/                   # Legacy SQL scripts (Reference only)
├── docker-compose.yml     # Container orchestration config
├── Dockerfile             # Python environment definition
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
🚀 Getting Started
You can run this project in two ways: Docker (Recommended) or Local Installation.

Option A: Run with Docker (Recommended) 🐳
The easiest way to run the project. No need to install Python or Postgres locally.

1. Clone the Repository:

PowerShell

git clone [https://github.com/Dvir216216/formula1-data-engineering-pipeline
Public
.git](https://github.com/Dvir216216/formula1-data-engineering-pipeline
Public
.git)
cd formula1-pipeline
2. Build & Start Services: This command spins up the Database and the Dashboard containers in the background.

PowerShell

docker-compose up --build -d
3. Run the ETL Pipeline: This command executes the pipeline inside the container to load data and create the Materialized Views.

PowerShell

docker-compose exec dashboard python src/reset_pipeline.py
Wait for the message: ✅ VIEW CREATED SUCCESSFULLY!

4. Access the Dashboard: Open your browser and navigate to: 👉 http://localhost:8501

Option B: Local Installation (Manual) 🛠️
Use this if you prefer running Python directly on your machine.

Prerequisites:

Python 3.12+ installed.

PostgreSQL installed and running locally.

1. Install Dependencies:

PowerShell

pip install -r requirements.txt
2. Configure Database: Ensure your local Postgres password matches the one in src/reset_pipeline.py (or update the script).

3. Run the Pipeline:

PowerShell

python src/reset_pipeline.py
4. Launch Dashboard:

PowerShell

streamlit run src/dashboard.py
⚡ Key Engineering Features
1. Robust Architecture (Microservices)
We separated the database (db) from the application (dashboard) using Docker Compose. Services communicate via an internal bridge network, ensuring isolation and security.

2. "Clean Slate" Reliability
We implemented a strict state-management protocol. The reset_pipeline.py script performs a full cascading teardown of tables and views before reloading, preventing "Zombie Data" and ensuring idempotency.

3. Performance Optimization (Materialized Views)
We tackled heavy JOIN operations (merging 5+ tables) by implementing Materialized Views.

Result: Query execution time dropped from 4.09ms to 0.16ms.

Method: Pre-computing complex joins and storing them physically on disk with specific indexes.

4. Embedded SQL Strategy
To resolve pathing issues across different OS environments (Windows vs. Linux), critical SQL logic is embedded directly within the Python ETL scripts, making the code "portable" and immune to FileNotFoundError.

📚 Documentation & Deep Dives
For a detailed breakdown of the engineering decisions, check the docs/ folder:

📄 [Level 1] Schema Design & Loading Strategy: How we modeled the Relational Database.

📄 [Level 2] Python ETL Architecture: Moving from scripts to a professional pipeline.

📄 [Level 3] Analytical Queries: Business insights extracted from the data.

📄 [Level 4] Database Optimization: Indexing strategies and Clustered Indexes.

📄 [Level 5] Materialized Views: Benchmarking performance (94% speedup).

📄 [Level 6] Infrastructure & Reliability: Docker containerization and deployment protocols.

👨‍💻 Author
Dvir - Data Engineering Student Built as a comprehensive Capstone Project demonstrating end-to-end Data Engineering capabilities.