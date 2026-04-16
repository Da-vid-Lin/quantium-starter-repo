import pandas as pd
import glob

# Load all CSV files from the data folder
files = glob.glob("data/*.csv")
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# Filter for Pink Morsels only
df = df[df["product"] == "pink morsel"]

# Calculate sales
df["sales"] = df["quantity"] * df["price"]

# Keep only the required columns
df = df[["sales", "date", "region"]]

# Save to output file
df.to_csv("tasks/task2/output.csv", index=False)

print("Done! Rows:", len(df))