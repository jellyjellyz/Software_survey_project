import sqlite3
from state_lookup_table import states
import plotly.plotly as py
import plotly.graph_objs as go

conn = sqlite3.connect('jobs.sqlite')
state_abbr = []
num_of_job = []
cur = conn.cursor()
statement = '''
    SELECT c.State, count(*)
    FROM Jobs AS j
        JOIN Company AS c
        ON j.CompanyId = c.Id
    GROUP BY c.State
    ORDER BY count(*) DESC
'''
# print(statement)
cur.execute(statement)

result = cur.fetchall()
# print(result)
state_abbr = [job[0] for job in result]
num_of_job = [job[1] for job in result]
# print(len(state_abbr))
# print(len(num_of_job))

data = [go.Bar(
    x=state_abbr,
    y=num_of_job,
    marker=dict(
    color=['rgba(222,45,38,0.8)']*10 + ['rgba(204,204,204,1)']*40
))]
layout = go.Layout(
    title='Number of positions by State'
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='Number of jobs by State')
    
