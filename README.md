# 🇮🇳 CivicLens India

Automated ETL Pipeline for Crime & Literacy Analytics 
on Indian Government Open Data

## Tech Stack
- Python
- Pandas
- MySQL
- SQLAlchemy
- Streamlit
- Plotly

## Project Structure
- `src/extract/` — Data extraction scripts
- `src/transform/` — Data cleaning scripts  
- `src/load/` — Database loading scripts
- `dashboard/` — Streamlit dashboard
- `sql/` — Database schema

## Data Sources
- NCRB Crime Data 2020–2022
- Census Literacy Data 2011
- Mid-Year Population 2022

## How to Run

### 1. Install dependencies
pip install -r requirements.txt

### 2. Setup database
Create civic_db in MySQL and run sql/schema.sql

### 3. Run pipeline
python src/pipeline/run_pipeline.py

### 4. Run dashboard
streamlit run dashboard/app.py

## Dashboard Features
- Crime rate analysis by state
- Literacy rate visualization
- Crime vs Literacy correlation
- Crime trends 2020-2022
- Interactive filters
- CSV download 