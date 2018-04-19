#####plot top 30 demanding software programming languages

import sqlite3
from nltk import word_tokenize
from nltk import FreqDist
import plotly.plotly as py
import plotly.graph_objs as go

def plot_top5_jobdescription():
    count = 0
    discrip_tokenize = []
    db_name = 'jobs.sqlite'
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    statement = '''
        SELECT JobDescription
        FROM Jobs
    '''
    cur.execute(statement)
    results = cur.fetchall()

    f = open('prog_language.txt', 'r')
    language = f.read()
    language = language.split('\n')
    # print(language)
    f.close()

    for result in results:
        result = result[0]
        words = word_tokenize(result)
        discrip_tokenize += words

    freq_dist = FreqDist()
    for token in discrip_tokenize:
        token = token.lower()
        if token in language:
            freq_dist[token] += 1
        
    language_name = []
    freq = []
    language_freq_list = freq_dist.most_common()
    for language in language_freq_list[:30]:
        language_name.append(language[0])
        freq.append(language[1])
    # print(language_name)
    # print(freq)

    data = [go.Bar(
        x=language_name,
        y=freq,
        marker=dict(
        color=['rgba(222,45,38,0.8)']*5 + ['rgba(204,204,204,1)']*25
    ))]
    layout = go.Layout(
        title='Programming Language Distribution',
        paper_bgcolor='rgb(242,242,242)',
        autosize=False,
        width=1000,
        height=600,
        margin=go.Margin(
            l=50,
            r=50,
            b=100,
            t=100,
        ),

    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='programming language distribution')

if __name__ == '__main__':
    plot_top5_jobdescription()
