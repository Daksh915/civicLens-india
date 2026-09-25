import pandas as pd
import os

# ── State name standardization map ──────────────────────────────
STATE_MAP = {
    "jammu & kashmir"               : "Jammu and Kashmir",
    "jammu and kashmir"             : "Jammu and Kashmir",
    "andaman & nicobar islands"     : "Andaman and Nicobar Islands",
    "andaman and nicobar islands"   : "Andaman and Nicobar Islands",
    "dadra & nagar haveli"          : "Dadra and Nagar Haveli",
    "dadra and nagar haveli"        : "Dadra and Nagar Haveli",
    "daman & diu"                   : "Daman and Diu",
    "daman and diu"                 : "Daman and Diu",
    "a & n islands"                 : "Andaman and Nicobar Islands",
    "d & n haveli"                  : "Dadra and Nagar Haveli",
}

def standardize_state(name):
    if pd.isna(name):
        return None
    cleaned = name.strip().lower()
    if cleaned in STATE_MAP:
        return STATE_MAP[cleaned]
    return name.strip().title()


def clean_literacy():
    filepath = "data/raw/literacy/literacy_raw.csv"

    # ── Step 1: File padhо ───────────────────────────────────────
    print("Step 1: Reading file...")
    df = pd.read_csv(filepath)
    print(f"Raw shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(df.head(3))

    # ── Step 2: Column names clean karo ─────────────────────────
    print("\nStep 2: Cleaning column names...")
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(' ', '_')
    )
    print(f"Clean columns: {df.columns.tolist()}")

    # ── Step 3: Rename columns ───────────────────────────────────
    print("\nStep 3: Renaming columns...")
    df = df.rename(columns={
        'state_name'    : 'state_name',
        'literacy_2011' : 'literacy_rate'
    })

    # ── Step 4: "na" strings → NaN ──────────────────────────────
    print("\nStep 4: Handling na values...")
    df['literacy_rate'] = df['literacy_rate'].replace('na', pd.NA)
    df['literacy_rate'] = df['literacy_rate'].replace('NA', pd.NA)
    df['literacy_rate'] = df['literacy_rate'].replace('n/a', pd.NA)

    # ── Step 5: Numeric convert karo ────────────────────────────
    print("\nStep 5: Converting to numeric...")
    df['literacy_rate'] = pd.to_numeric(
        df['literacy_rate'],
        errors='coerce'
    )

    # ── Step 6: State names standardize karo ────────────────────
    print("\nStep 6: Standardizing state names...")
    df['state_name'] = df['state_name'].apply(standardize_state)

    # ── Step 7: All India row hata do ───────────────────────────
    print("\nStep 7: Removing All India row...")
    df = df[~df['state_name'].str.lower().str.contains('all india', na=False)]

    # ── Step 8: Null rows drop karo ─────────────────────────────
    print("\nStep 8: Dropping null rows...")
    before = len(df)
    df = df.dropna(subset=['literacy_rate'])
    after = len(df)
    print(f"Rows dropped: {before - after}")

    # ── Step 9: Extra columns add karo ──────────────────────────
    print("\nStep 9: Adding metadata columns...")
    df['data_year']   = 2011
    df['source_name'] = 'census_2011_literacy'
    df['ingested_at'] = pd.Timestamp.now()

    # ── Step 10: Reset index ─────────────────────────────────────
    df = df.reset_index(drop=True)

    # ── Step 11: Final check ─────────────────────────────────────
    print("\n" + "="*50)
    print("FINAL CLEAN DATA:")
    print("="*50)
    print(f"Total rows: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    print("\nNull check:")
    print(df.isnull().sum())
    print("\nSample data:")
    print(df.head(10))

    return df


def save_clean_literacy(df):
    # ── Staging folder banao agar nahi hai ──────────────────────
    os.makedirs("data/staging", exist_ok=True)
    out_path = "data/staging/literacy_clean.csv"
    df.to_csv(out_path, index=False)
    print(f"\n✅ Clean file saved: {out_path}")
    return out_path


if __name__ == "__main__":
    df = clean_literacy()
    save_clean_literacy(df)
    print("\n🎉 Literacy cleaning complete!")