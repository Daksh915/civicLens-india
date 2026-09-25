import pandas as pd
import os

# ── State name standardization ───────────────────────────────────
STATE_MAP = {
    "jammu & kashmir"              : "Jammu and Kashmir",
    "jammu and kashmir"            : "Jammu and Kashmir",
    "andaman & nicobar islands"    : "Andaman and Nicobar Islands",
    "andaman and nicobar islands"  : "Andaman and Nicobar Islands",
    "dadra & nagar haveli"         : "Dadra and Nagar Haveli",
    "dadra and nagar haveli"       : "Dadra and Nagar Haveli",
    "daman & diu"                  : "Daman and Diu",
    "daman and diu"                : "Daman and Diu",
    "d & n haveli"                 : "Dadra and Nagar Haveli",
    "a & n islands"                : "Andaman and Nicobar Islands",
    "nct of delhi"                 : "Delhi",
    "delhi"                        : "Delhi",
}

def standardize_state(name):
    if pd.isna(name):
        return None
    cleaned = name.strip().lower()
    if cleaned in STATE_MAP:
        return STATE_MAP[cleaned]
    return name.strip().title()


def clean_crime():
    filepath = "data/raw/crime/crime_raw.csv"

    # ── Step 1: File padho ───────────────────────────────────────
    print("Step 1: Reading file...")
    df = pd.read_csv(filepath)
    print(f"Raw shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print("\nFirst 3 rows:")
    print(df.head(3))

    # ── Step 2: Column names clean karo ─────────────────────────
    print("\nStep 2: Cleaning column names...")
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(' ', '_')
        .str.replace('(', '')
        .str.replace(')', '')
        .str.replace('/', '_')
    )
    print(f"Clean columns: {df.columns.tolist()}")

    # ── Step 3: Rename important columns ────────────────────────
    print("\nStep 3: Renaming columns...")
    df = df.rename(columns={
        'state_ut'                                    : 'state_name',
        'sl._no.'                                     : 'sl_no',
        'mid-year_projected_population_in_lakhs_2022' : 'population_lakhs_2022',
        'rate_of_cognizable_crimes_ipc_2022'          : 'crime_rate_per_lakh_2022',
        'chargesheeting_rate_2022'                    : 'chargesheeting_rate_2022',
    })
    print(f"Renamed columns: {df.columns.tolist()}")

    # ── Step 4: sl_no column drop karo ──────────────────────────
    print("\nStep 4: Dropping unnecessary columns...")
    if 'sl_no' in df.columns:
        df = df.drop(columns=['sl_no'])

    # ── Step 5: Wide to Long format ─────────────────────────────
    print("\nStep 5: Converting wide to long format...")

    # Pehle check karo kaunse year columns hain
    year_cols = [col for col in df.columns if col in ['2020', '2021', '2022']]
    print(f"Year columns found: {year_cols}")

    # Non-year columns
    id_cols = [col for col in df.columns if col not in year_cols]
    print(f"ID columns: {id_cols}")

    # Melt karo
    df_long = pd.melt(
        df,
        id_vars=id_cols,
        value_vars=year_cols,
        var_name='year',
        value_name='total_crimes'
    )

    print(f"Shape after melt: {df_long.shape}")

    # ── Step 6: Data types fix karo ─────────────────────────────
    print("\nStep 6: Fixing data types...")
    df_long['year']        = pd.to_numeric(df_long['year'], errors='coerce').astype('Int64')
    df_long['total_crimes'] = pd.to_numeric(
        df_long['total_crimes'].astype(str).str.replace(',', ''),
        errors='coerce'
    )
    df_long['population_lakhs_2022']     = pd.to_numeric(df_long['population_lakhs_2022'], errors='coerce')
    df_long['crime_rate_per_lakh_2022']  = pd.to_numeric(df_long['crime_rate_per_lakh_2022'], errors='coerce')
    df_long['chargesheeting_rate_2022']  = pd.to_numeric(df_long['chargesheeting_rate_2022'], errors='coerce')

    # ── Step 7: State names standardize karo ────────────────────
    print("\nStep 7: Standardizing state names...")
    df_long['state_name'] = df_long['state_name'].apply(standardize_state)

    # ── Step 8: Total/All India rows hata do ────────────────────
    print("\nStep 8: Removing total/summary rows...")
    df_long = df_long[
        ~df_long['state_name'].str.lower().str.contains('total', na=False)
    ]
    df_long = df_long[
        ~df_long['state_name'].str.lower().str.contains('all india', na=False)
    ]

    # ── Step 9: Null rows drop karo ─────────────────────────────
    print("\nStep 9: Dropping null rows...")
    before = len(df_long)
    df_long = df_long.dropna(subset=['state_name', 'year', 'total_crimes'])
    after = len(df_long)
    print(f"Rows dropped: {before - after}")

    # ── Step 10: Duplicates remove karo ─────────────────────────
    print("\nStep 10: Removing duplicates...")
    before = len(df_long)
    df_long = df_long.drop_duplicates(subset=['state_name', 'year'])
    after = len(df_long)
    print(f"Duplicates removed: {before - after}")

    # ── Step 11: Metadata add karo ──────────────────────────────
    print("\nStep 11: Adding metadata...")
    df_long['source_name'] = 'ncrb_crime_2022'
    df_long['ingested_at'] = pd.Timestamp.now()

    # ── Step 12: Sort karo ──────────────────────────────────────
    df_long = df_long.sort_values(
        ['state_name', 'year']
    ).reset_index(drop=True)

    # ── Final output ─────────────────────────────────────────────
    print("\n" + "="*50)
    print("FINAL CLEAN CRIME DATA:")
    print("="*50)
    print(f"Total rows    : {len(df_long)}")
    print(f"Columns       : {df_long.columns.tolist()}")
    print(f"Years covered : {sorted(df_long['year'].dropna().unique().tolist())}")
    print(f"States        : {df_long['state_name'].nunique()} unique")
    print("\nNull check:")
    print(df_long.isnull().sum())
    print("\nSample data:")
    print(df_long.head(9))

    return df_long


def save_clean_crime(df):
    os.makedirs("data/staging", exist_ok=True)
    out_path = "data/staging/crime_clean.csv"
    df.to_csv(out_path, index=False)
    print(f"\n✅ Clean file saved: {out_path}")
    return out_path


if __name__ == "__main__":
    df = clean_crime()
    save_clean_crime(df)
    print("\n🎉 Crime cleaning complete!")