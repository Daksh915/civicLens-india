import sys
sys.path.append(".")
import pandas as pd
from sqlalchemy import text
from src.utils.db_connection import get_engine

def load_dim_state(states):
    engine = get_engine()
    conn = engine.connect()
    for name in states:
        conn.execute(text("INSERT IGNORE INTO dim_state (state_name) VALUES (:name)"), {"name": name})
    conn.commit()
    conn.close()
    print("dim_state done:", len(states), "states")

def load_dim_year(years):
    engine = get_engine()
    conn = engine.connect()
    for y in years:
        conn.execute(text("INSERT IGNORE INTO dim_year (year) VALUES (:year)"), {"year": int(y)})
    conn.commit()
    conn.close()
    print("dim_year done:", len(years), "years")

if __name__ == "__main__":
    df = pd.read_csv("data/staging/master_clean.csv")

    states = df['state_name'].dropna().unique().tolist()
    years = df['year'].dropna().unique().tolist()

    print("states found:", len(states))
    print("years found:", years)

    load_dim_state(states)
    load_dim_year(years)

    print("dimensions loaded😃")