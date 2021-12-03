import pandas as pd
from datetime import timedelta
import plotly.express as px
import dash
from dash import dcc
from dash import html


df = pd.read_csv('SAP_schedule_data.csv')

df["ClassDate"]= pd.to_datetime(df["ClassDate"])
df['date2']=df['ClassDate']+timedelta(days=0.95)
df['ClassUnique']=df['ClassGrade']+'_'+df['Subdivision']

fig = px.timeline(df, x_start="ClassDate", x_end="date2", y="ClassUnique", color="InstructorName", template='seaborn')
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

app = dash.Dash()
server = app.server

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
