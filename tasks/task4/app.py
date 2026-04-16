import pandas as pd
import dash
from dash import html, dcc, callback, Output, Input
import plotly.express as px

df = pd.read_csv("tasks/task2/output.csv")
df["date"] = pd.to_datetime(df["date"])
df["sales"] = pd.to_numeric(df["sales"])
df = df.sort_values("date")

price_increase_date = pd.Timestamp("2021-01-15").timestamp() * 1000

app = dash.Dash(__name__, external_stylesheets=[
    "https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap"
])

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "background": "linear-gradient(135deg, #0f0c29, #302b63, #24243e)",
        "fontFamily": "'DM Sans', sans-serif",
        "padding": "48px 40px",
    },
    children=[

        # Header
        html.Div(
            style={"marginBottom": "48px"},
            children=[
                html.Div(
                    "SOUL FOODS ANALYTICS",
                    style={
                        "color": "#ff6eb4",
                        "fontSize": "11px",
                        "fontWeight": "500",
                        "letterSpacing": "4px",
                        "marginBottom": "12px",
                        "opacity": "0.9"
                    }
                ),
                html.H1(
                    "Pink Morsel Sales",
                    style={
                        "fontFamily": "'DM Serif Display', serif",
                        "color": "#ffffff",
                        "fontSize": "52px",
                        "margin": "0 0 12px 0",
                        "lineHeight": "1.1",
                        "fontWeight": "400",
                    }
                ),
                html.P(
                    "Analysing the impact of the January 2021 price increase across all regions",
                    style={"color": "rgba(255,255,255,0.45)", "fontSize": "15px", "margin": "0", "fontWeight": "300"}
                ),
            ]
        ),

        # Stats row
        html.Div(
            style={"display": "flex", "gap": "16px", "marginBottom": "32px"},
            children=[
                html.Div(
                    style={
                        "background": "rgba(255,255,255,0.06)",
                        "border": "1px solid rgba(255,255,255,0.1)",
                        "borderRadius": "12px",
                        "padding": "20px 28px",
                        "flex": "1"
                    },
                    children=[
                        html.Div("Total Sales", style={"color": "rgba(255,255,255,0.4)", "fontSize": "12px", "letterSpacing": "2px", "marginBottom": "6px"}),
                        html.Div(id="stat-total", style={"color": "#fff", "fontSize": "26px", "fontFamily": "'DM Serif Display', serif"})
                    ]
                ),
                html.Div(
                    style={
                        "background": "rgba(255,255,255,0.06)",
                        "border": "1px solid rgba(255,255,255,0.1)",
                        "borderRadius": "12px",
                        "padding": "20px 28px",
                        "flex": "1"
                    },
                    children=[
                        html.Div("Peak Day", style={"color": "rgba(255,255,255,0.4)", "fontSize": "12px", "letterSpacing": "2px", "marginBottom": "6px"}),
                        html.Div(id="stat-peak", style={"color": "#fff", "fontSize": "26px", "fontFamily": "'DM Serif Display', serif"})
                    ]
                ),
                html.Div(
                    style={
                        "background": "rgba(255,255,255,0.06)",
                        "border": "1px solid rgba(255,110,180,0.3)",
                        "borderRadius": "12px",
                        "padding": "20px 28px",
                        "flex": "1"
                    },
                    children=[
                        html.Div("Price Increase", style={"color": "rgba(255,255,255,0.4)", "fontSize": "12px", "letterSpacing": "2px", "marginBottom": "6px"}),
                        html.Div("15 Jan 2021", style={"color": "#ff6eb4", "fontSize": "26px", "fontFamily": "'DM Serif Display', serif"})
                    ]
                ),
            ]
        ),

        # Chart card
        html.Div(
            style={
                "background": "rgba(255,255,255,0.05)",
                "border": "1px solid rgba(255,255,255,0.1)",
                "borderRadius": "20px",
                "padding": "32px",
                "backdropFilter": "blur(10px)",
            },
            children=[

                # Region filter
                html.Div(
                    style={"display": "flex", "alignItems": "center", "justifyContent": "space-between", "marginBottom": "28px"},
                    children=[
                        html.Span("Sales Over Time", style={"color": "rgba(255,255,255,0.7)", "fontSize": "13px", "letterSpacing": "2px"}),
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": "All", "value": "all"},
                                {"label": "North", "value": "north"},
                                {"label": "East", "value": "east"},
                                {"label": "South", "value": "south"},
                                {"label": "West", "value": "west"},
                            ],
                            value="all",
                            inline=True,
                            inputStyle={"display": "none"},
                            labelStyle={
                                "padding": "6px 16px",
                                "borderRadius": "20px",
                                "border": "1px solid rgba(255,255,255,0.15)",
                                "color": "rgba(255,255,255,0.55)",
                                "fontSize": "13px",
                                "cursor": "pointer",
                                "marginLeft": "8px",
                                "transition": "all 0.2s",
                            }
                        )
                    ]
                ),

                dcc.Graph(id="sales-chart", config={"displayModeBar": False})
            ]
        )
    ]
)


@callback(
    Output("sales-chart", "figure"),
    Output("stat-total", "children"),
    Output("stat-peak", "children"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered_df = df.groupby("date", as_index=False)["sales"].sum()
    else:
        filtered_df = df[df["region"] == selected_region].groupby("date", as_index=False)["sales"].sum()

    total = f"${filtered_df['sales'].sum():,.0f}"
    peak_date = filtered_df.loc[filtered_df["sales"].idxmax(), "date"].strftime("%d %b %Y")

    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        labels={"date": "Date", "sales": "Sales ($)"},
    )

    fig.update_traces(
        line={"color": "#ff6eb4", "width": 2},
        fill="tozeroy",
        fillcolor="rgba(255,110,180,0.08)"
    )

    fig.add_vline(
        x=price_increase_date,
        line_dash="dot",
        line_color="rgba(255,110,180,0.5)",
        line_width=1.5,
        annotation_text="↑ Price increase",
        annotation_font_color="#ff6eb4",
        annotation_font_size=12,
        annotation_position="top right"
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "rgba(255,255,255,0.5)", "family": "DM Sans"},
        xaxis={
            "gridcolor": "rgba(255,255,255,0.05)",
            "showline": False,
            "tickfont": {"size": 11},
            "title": {"text": "Date", "font": {"color": "rgba(255,255,255,0.3)", "size": 11}},
        },
        yaxis={
            "gridcolor": "rgba(255,255,255,0.05)",
            "showline": False,
            "tickfont": {"size": 11},
            "title": {"text": "Sales ($)", "font": {"color": "rgba(255,255,255,0.3)", "size": 11}},
        },
        margin={"t": 10, "b": 40, "l": 50, "r": 20},
        height=420,
        hovermode="x unified",
    )

    return fig, total, peak_date


if __name__ == "__main__":
    app.run(debug=True)