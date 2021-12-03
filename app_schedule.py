import pandas as pd
from datetime import timedelta
import pyodbc
import plotly.express as px
import dash
from dash import dcc
from dash import html

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-4UMM3V8\SQLEXPRESS;'
                      'Database=SAP_test;'
                      'Trusted_Connection=yes;')


sql_query = pd.read_sql_query(''' 
                              select * from SAP_test.dbo.vwClassScheduleDetail
                              '''
                              ,conn) # here, the 'conn' is the variable that contains your database connection information from step 2

df = pd.DataFrame(sql_query)
# df.to_csv (r'C:\Users\franc\OneDrive\2.PythonProjects\SAP_tutoring\exported_data.csv', index = False) # place 'r' before the path name
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
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
