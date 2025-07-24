import pandas as pd
import plotly.express as px
import os

# Create dummy data
df = pd.DataFrame({'x': ['A', 'B', 'C'], 'y': [1, 2, 3]})

# Create a bar plot
fig = px.bar(df, x='x', y='y')

# Create the data folder if not exists
os.makedirs("data", exist_ok=True)

# Generate the absolute file path
path = os.path.abspath("data/last_plot.html")

# Save the plot
fig.write_html(path)

print(f"✅ Plot saved to: {path}")
