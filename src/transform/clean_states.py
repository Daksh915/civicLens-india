import pandas as pd
import os

def join_datasets():

    # ── Step 1: Dono clean files padho ──────────────────────────
    print("Step 1: Reading clean files...")
    crime_df    = pd.read_csv("data/staging/crime_clean.csv")
    literacy_df = pd.read_csv("data/staging/literacy_clean.csv")

    print(f"Crime rows    : {len(crime_df)}")
    print(f"Literacy rows : {len(literacy_df)}")
    print(f"\nCrime states    : {sorted(crime_df['state_name'].unique().tolist())}")
    print(f"\nLiteracy states : {sorted(literacy_df['state_name'].unique().tolist())}")

    # ── Step 2: Join karo ───────────────────────────────────────
    print("\nStep 2: Joining datasets on state_name...")
    merged = crime_df.merge(
        literacy_df[['state_name', 'literacy_rate', 'data_year']],
        on='state_name',
        how='left'
    )
    merged = merged.rename(columns={'data_year': 'literacy_year'})

    # ── Step 3: Match check karo ────────────────────────────────
    print("\nStep 3: Checking matches...")
    matched   = merged['literacy_rate'].notna().sum()
    unmatched = merged['literacy_rate'].isna().sum()
    print(f"Matched rows   : {matched}")
    print(f"Unmatched rows : {unmatched}")

    # Unmatched states dikhao
    if unmatched > 0:
        unmatched_states = merged[
            merged['literacy_rate'].isna()
        ]['state_name'].unique()
        print(f"\n⚠️  These states did NOT match:")
        for s in unmatched_states:
            print(f"   → {s}")

    # ── Step 4: Final columns organize karo ─────────────────────
    print("\nStep 4: Organizing final columns...")
    merged = merged[[
        'state_name',
        'year',
        'total_crimes',
        'population_lakhs_2022',
        'crime_rate_per_lakh_2022',
        'chargesheeting_rate_2022',
        'literacy_rate',
        'literacy_year',
        'source_name',
        'ingested_at'
    ]]

    # ── Final output ─────────────────────────────────────────────
    print("\n" + "="*50)
    print("FINAL MASTER DATASET:")
    print("="*50)
    print(f"Total rows : {len(merged)}")
    print(f"Columns    : {merged.columns.tolist()}")
    print("\nNull check:")
    print(merged.isnull().sum())
    print("\nSample data:")
    print(merged.head(6))

    return merged


def save_master(df):
    os.makedirs("data/staging", exist_ok=True)
    out_path = "data/staging/master_clean.csv"
    df.to_csv(out_path, index=False)
    print(f"\n✅ Master file saved: {out_path}")
    return out_path


if __name__ == "__main__":
    df = join_datasets()
    save_master(df)
    print("\n🎉 Join complete!")