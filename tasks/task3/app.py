import pandas as pd
import dash
from dash import html, dcc
import plotly.express as px

# Load the processed data from task 2
df = pd.read_csv("tasks/task2/output.csv")

# Sort by date so the line chart flows left to right chronologically
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Build the line chart
fig = px.line(
    df,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Sales ($)"}
)

# Add a vertical line to mark the price increase on 15th Jan 2021
price_increase_date = pd.Timestamp("2021-01-15").timestamp() * 1000  # convert to milliseconds
fig.add_vline(
    x=price_increase_date,
    line_dash="dash",
    line_color="red",
    annotation_text="Price increase",
    annotation_position="top right"
)

# Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualiser"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)