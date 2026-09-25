import pandas as pd

crime = pd.read_csv("data/staging/crime_clean.csv")
literacy = pd.read_csv("data/staging/literacy_clean.csv")

crime_states = set(crime['state_name'].unique())
literacy_states = set(literacy['state_name'].unique())

print("States in crime but not in literacy:")
for s in sorted(crime_states - literacy_states):
    print(" ->", s)

print("\nStates in literacy but not in crime:")
for s in sorted(literacy_states - crime_states):
    print(" ->", s)