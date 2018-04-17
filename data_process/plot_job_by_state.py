########get jobs(title, lat, lon) by state, and save them in a dictionary as class JobinState
import plotly.plotly as py
from plotly.graph_objs import *
import sqlite3
# from state_lookup_table import states
from state_short import states
from random import randint

from secrets import mapbox_access_token
import colorlover as cl
from JobinStateClass import JobinState
from symbol_by_type import color


conn = sqlite3.connect('jobs.sqlite')
geo_by_state = {}
color_list = cl.scales['10']['div']['Spectral']

for idx, key in enumerate(states):
    cur = conn.cursor()
    statement = '''
            SELECT j.Title, c.GeoLat, c.GeoLon, j.Jobtype
            FROM Jobs AS j
                JOIN Company AS c
                ON j.CompanyId = c.Id
            WHERE c.State = '{}'
    '''.format(key)
    cur.execute(statement)

    result = cur.fetchall()
    # print(result)
    if result == []:
        continue
    titles = []
    lats = []
    lons = []
    jobtype = []
    for aresult in result:
        titles.append('{}, {}'.format(aresult[0], aresult[3]))
        lats.append(aresult[1])
        lons.append(aresult[2])
        jobtype.append(aresult[3])
    geo_by_state[key] = JobinState(states[key], titles, lats, lons, jobtype)
# print(geo_by_state['AL'])
for key in geo_by_state:
    lon_vals = geo_by_state[key].lons
    lat_vals = geo_by_state[key].lats
    text_vals = geo_by_state[key].titles
    colors = [color_list[color[thetype]] for thetype in geo_by_state[key].jobtype]

    data = [Scattermapbox(
                    lon = lon_vals,
                    lat = lat_vals,
                    name = 'Jobs in {}'.format(key),
                    mode='markers',
                    marker = Marker(
                        color = 'rgb(5, 5, 5)',
                        size = 13,
                        symbol = 'circle',
                        opacity=0.7,
                    ),hoverinfo='none'
                    ),
                    Scattermapbox(
                    lon = lon_vals,
                    lat = lat_vals,
                    text = text_vals,
                    mode = 'markers',
                    marker = Marker(
                        color = colors,
                        size = 10,
                        symbol = 'circle',
                        opacity=1,
                    ),hoverinfo='text'
                    )]
    layout = Layout(
            autosize=False,
            width=1000,
            height=600,
            margin = dict(l = 0, r = 0, t = 50, b = 0),
            showlegend=False,
            paper_bgcolor='rgb(242,242,242)',
            title = 'Jobs in {}'.format(geo_by_state[key].state),
            hovermode='closest',
            mapbox=dict(
                        accesstoken=mapbox_access_token,
                        style='light',
                        bearing=0,
                        center=dict(
                            lat=(max(lat_vals)+min(lat_vals))*0.5,
                            lon=(max(lon_vals)+min(lon_vals))*0.5
                        ),

                        pitch=0,
                        zoom=5.8
                    ),
                )
    data = Data(data)
    fig = dict(data = data, layout = layout)
    py.plot(fig, filename = 'jobs in {}'.format(geo_by_state[key].state))