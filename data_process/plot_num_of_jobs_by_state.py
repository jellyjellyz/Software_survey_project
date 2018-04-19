#######plot num of jobs in each state on a histogram

import sqlite3
from state_lookup_table import states
import plotly.plotly as py
import plotly.graph_objs as go
from state_lookup_table import states

def plot_num_of_jobs_by_state():
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
    state_abbr = [states[job[0]] for job in result]
    num_of_job = [job[1] for job in result]
    percent_of_job=[round(num*100/sum(num_of_job), 2) for num in num_of_job]
    # print(len(state_abbr))
    # print(len(num_of_job))

    data = [go.Bar(
        x=state_abbr,
        y=percent_of_job,
        marker=dict(
        color=['rgba(222,45,38,0.8)']*10 + ['rgba(204,204,204,1)']*40
    ))]
    layout = go.Layout(
        autosize=False,
        width=1000,
        height=600,
        margin=go.Margin(
            l=50,
            r=50,
            b=100,
            t=100,
        ),
        paper_bgcolor='rgb(242,242,242)',
        title='Number of positions by State',
        yaxis=dict(
        title='% (num of position per state/sum of all positions)'
        ))
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='Number of jobs by State')

if __name__ == '__main__':
    plot_num_of_jobs_by_state()
    
