###########plot all jobs on a single map, and plot jobs in different color correponding to different state.

import plotly.plotly as py
from plotly.graph_objs import *
import sqlite3
from state_lookup_table import states
from secrets import mapbox_access_token
import colorlover as cl

conn = sqlite3.connect('jobs.sqlite')
color_list = (cl.scales['10']['div']['Spectral'] + cl.scales['10']['div']['RdYlGn'])*3
data_list = []
for idx, key in enumerate(states):
    cur = conn.cursor()
    statement = '''
            SELECT j.Title, c.GeoLat, c.GeoLon
            FROM Jobs AS j
                JOIN Company AS c
                ON j.CompanyId = c.Id
            WHERE c.State = '{}'
    '''.format(key)
    # print(statement)
    cur.execute(statement)

    result = cur.fetchall()
    # print(result)
    if result == []:
        continue

    lat_vals = []
    lon_vals = []
    text_vals = []
    for acompany in result:
        lat_vals.append(acompany[1])
        lon_vals.append(acompany[2])
        text_vals.append(acompany[0])
    data_list += [Scattermapbox(
                    lon = lon_vals,
                    lat = lat_vals,
                    text = text_vals,
                    mode = 'markers',
                    name = 'Jobs in {}'.format(key),
                    marker = Marker(
                        color = color_list[idx],
                        size = 5,
                        symbol = 'circle',
                    ))]

layout = Layout(
            autosize=True,
            hovermode='closest',
            mapbox=dict(
                        accesstoken=mapbox_access_token,
                        style='dark',
                        bearing=0,
                        center=dict(
                            lat=37.0902,
                            lon=-95.7129
                        ),
                        pitch=0,
                        zoom=3.6
                    ),
                )

data = Data(data_list)
fig = dict(data = data, layout = layout)
py.plot(fig, filename = 'jobs in America')





