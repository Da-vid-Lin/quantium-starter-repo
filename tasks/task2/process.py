import pandas as pd
import glob

# Load and combine all CSV files
files = glob.glob("data/*.csv")
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# Only keep Pink Morsel rows
is_pink_morsel = df["product"] == "pink morsel"
df = df[is_pink_morsel].copy()

# Strip $ sign from price and convert to number
df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)

# Calculate total sales (quantity × price)
df["sales"] = df["quantity"] * df["price"]

# Keep only the required columns
df = df[["sales", "date", "region"]]

# Save to output file
df.to_csv("tasks/task2/output.csv", index=False)

print(f"Done! {len(df)} rows written to output.csv")