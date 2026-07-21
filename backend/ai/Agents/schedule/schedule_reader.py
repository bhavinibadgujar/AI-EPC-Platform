import pandas as pd

df = pd.read_csv("dataset/schedules/schedule_1.csv")

date_columns = [
    "Planned Start",
    "Planned Finish",
    "Actual Finish"
]

for col in date_columns:
    df[col] = pd.to_datetime(
        df[col],
        format="%d-%m-%Y"
    )

print(df)
print(df.dtypes)