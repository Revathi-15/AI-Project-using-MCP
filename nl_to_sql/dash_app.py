import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os

# Paths
CSV_PATH = os.path.join("data", "last_result.csv")

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Claude-Powered SQL Dashboard"

app.layout = html.Div([
    html.H2("\U0001F9E0 Claude-Powered SQL Dashboard", style={"color": "#222"}),
    html.P("Ask Claude a question (via MCP), and the dashboard auto-updates.", style={"marginBottom": "20px"}),

    dcc.Dropdown(id='chart-type',
                 options=[
                     {"label": "Bar", "value": "bar"},
                     {"label": "Line", "value": "line"},
                     {"label": "Scatter", "value": "scatter"}
                 ],
                 value='bar',
                 clearable=False,
                 style={"width": "200px", "marginBottom": "10px"}),

    dcc.Graph(id="main-graph"),

    dcc.Interval(
        id='interval-update',
        interval=3*1000,  # refresh every 3 sec
        n_intervals=0
    ),

    html.Div(id="status", style={"marginTop": "20px", "fontFamily": "monospace"})
])

@app.callback(
    [Output("main-graph", "figure"),
     Output("status", "children")],
    [Input("interval-update", "n_intervals"),
     Input("chart-type", "value")]
)
def update_dashboard(_, chart_type):
    if not os.path.exists(CSV_PATH):
        return px.line(), "Waiting for Claude to generate a result..."

    try:
        df = pd.read_csv(CSV_PATH)
        if df.empty:
            return px.line(), "Data is empty. Waiting for Claude..."

        # Try to pick suitable x/y columns
        x = df.columns[0]
        y = df.columns[1] if df.shape[1] > 1 else df.columns[0]

        if chart_type == "bar":
            fig = px.bar(df, x=x, y=y, hover_data=df.columns)
        elif chart_type == "line":
            fig = px.line(df, x=x, y=y, hover_data=df.columns)
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x, y=y, hover_data=df.columns)
        else:
            fig = px.line()

        fig.update_layout(margin=dict(l=20, r=20, t=40, b=40))
        return fig, f"Updated from: {CSV_PATH}"

    except Exception as e:
        return px.line(), f"Error: {e}"

if __name__ == "__main__":
    app.run(debug=True, port=8050)
