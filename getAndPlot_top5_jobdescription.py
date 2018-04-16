import sqlite3
from nltk import word_tokenize
from nltk import FreqDist
import plotly.plotly as py
import plotly.graph_objs as go


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
for language in language_freq_list[:50]:
    language_name.append(language[0])
    freq.append(language[1])
# print(language_name)
# print(freq)

data = [go.Bar(
    x=language_name,
    y=freq,
    marker=dict(
    color=['rgba(222,45,38,0.8)']*5 + ['rgba(204,204,204,1)']*45
))]
layout = go.Layout(
    title='Programming Language Distribution',
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='programming language distribution')
