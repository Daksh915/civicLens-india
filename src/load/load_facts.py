import sys
sys.path.append(".")
import pandas as pd
from sqlalchemy import text
from src.utils.db_connection import get_engine

def get_state_id(conn, state_name):
    result = conn.execute(text("SELECT state_id FROM dim_state WHERE state_name = :name"), {"name": state_name})
    row = result.fetchone()
    return row[0] if row else None

def get_year_id(conn, year):
    result = conn.execute(text("SELECT year_id FROM dim_year WHERE year = :year"), {"year": int(year)})
    row = result.fetchone()
    return row[0] if row else None

def load_fact_crime():
    df = pd.read_csv("data/staging/master_clean.csv")
    print("rows to load:", len(df))

    engine = get_engine()
    conn = engine.connect()

    loaded = 0
    skipped = 0

    for _, row in df.iterrows():
        state_id = get_state_id(conn, row['state_name'])
        year_id = get_year_id(conn, row['year'])

        if state_id is None or year_id is None:
            skipped += 1
            continue

        conn.execute(text("""
            INSERT IGNORE INTO fact_crime
            (state_id, year_id, total_crimes, population_lakhs_2022,
            crime_rate_per_lakh_2022, chargesheeting_rate_2022,
            literacy_rate, literacy_year, source_name)
            VALUES
            (:state_id, :year_id, :total_crimes, :population_lakhs_2022,
            :crime_rate_per_lakh_2022, :chargesheeting_rate_2022,
            :literacy_rate, :literacy_year, :source_name)
        """), {
            "state_id"                : state_id,
            "year_id"                 : year_id,
            "total_crimes"            : int(row['total_crimes']) if pd.notna(row['total_crimes']) else None,
            "population_lakhs_2022"   : float(row['population_lakhs_2022']) if pd.notna(row['population_lakhs_2022']) else None,
            "crime_rate_per_lakh_2022": float(row['crime_rate_per_lakh_2022']) if pd.notna(row['crime_rate_per_lakh_2022']) else None,
            "chargesheeting_rate_2022": float(row['chargesheeting_rate_2022']) if pd.notna(row['chargesheeting_rate_2022']) else None,
            "literacy_rate"           : float(row['literacy_rate']) if pd.notna(row['literacy_rate']) else None,
            "literacy_year"           : int(row['literacy_year']) if pd.notna(row['literacy_year']) else None,
            "source_name"             : str(row['source_name']) if pd.notna(row['source_name']) else None,
        })
        loaded += 1

    conn.commit()
    conn.close()

    print("loaded:", loaded, "rows")
    print("skipped:", skipped, "rows")
    print("fact_crime done👍")

if __name__ == "__main__":
    load_fact_crime()
    
    
    
    