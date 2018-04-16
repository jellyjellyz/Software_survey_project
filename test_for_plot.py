import plotly.plotly as py
from plotly.graph_objs import *
import sqlite3
from state_lookup_table import states
from secrets import mapbox_access_token



def get_company_by_state(state_abbr):
    conn = sqlite3.connect('jobs.sqlite')
    cur = conn.cursor()

    # statement for specific state
    statement = '''
            SELECT j.Title, c.GeoLat, c.GeoLon
            FROM Jobs AS j
                JOIN Company AS c
                ON j.CompanyId = c.Id
            WHERE c.State = '{}'
    '''.format(state_abbr)

    # statement for all jobs
    # statement = '''
    #         SELECT j.Title, c.GeoLat, c.GeoLon
    #         FROM Jobs AS j
    #             JOIN Company AS c
    #             ON j.CompanyId = c.Id
    # '''

    cur.execute(statement)
    result = cur.fetchall()
    # print(result)
    # for aresult in result:
        # print(aresult)
    conn.close()
    return result

# get_company_by_state('CA')

def plot_sites_for_state(state_abbr):
    lat_vals = []
    lon_vals = []
    text_vals = []
    company_list = get_company_by_state(state_abbr)
    lat_low_bound = 24.7433195
    lat_high_bound = 49.3457868
    lon_low_bound = -124.7844079
    lon_high_bound = -66.9513812

    for acompany in company_list:
        if acompany[1] >= lat_low_bound \
            and acompany[1] <= lat_high_bound \
            and acompany[2] >= lon_low_bound \
            and acompany[2] <= lon_high_bound:
            lat_vals.append(acompany[1])
            lon_vals.append(acompany[2])
            text_vals.append(acompany[0])
    
    min_lat = 10000
    max_lat = -10000
    min_lon = 10000
    max_lon = -10000

    for v in lat_vals:
        if v < min_lat:
            min_lat = v
        if v > max_lat:
            max_lat = v
    for v in lon_vals:
        if v < min_lon:
            min_lon = v
        if v > max_lon:
            max_lon = v

    max_range = max(abs(max_lat - min_lat), abs(max_lon - min_lon))
    padding = max_range * .10
    lat_axis = [min_lat - padding, max_lat + padding]
    lon_axis = [min_lon - padding, max_lon + padding]

    center_lat = (max_lat+min_lat) / 2
    center_lon = (max_lon+min_lon) / 2
    print(center_lat)
    print(center_lon)

    layout = Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(
                    lat=center_lat,
                    lon=center_lon
                ),
                pitch=0,
                zoom=3.5
            ),
        )

    # layout = dict(
    #         title = 'Software Jobs in {}'.format(states[state_abbr.upper()]),
    #         geo = dict(
    #             scope='usa',
    #             projection=dict( type='albers usa' ),
    #             showlakes = True,
    #             showland = True,
    #             lakecolor = "rgb(51, 153, 255)",
    #             landcolor = "rgb(250, 223, 150)",
    #             subunitcolor = "grey",
    #             countrycolor = "rgb(217, 100, 217)",
    #             lataxis = {'range': lat_axis},
    #             lonaxis = {'range': lon_axis},
    #             center= {'lat': center_lat, 'lon': center_lon },
    #             countrywidth = 2,
    #             subunitwidth = 2
    #         ),
    #     )


    data = Data([ Scattermapbox(
            type = 'scattermapbox',
            # locationmode = 'USA-states',
            lon = lon_vals,
            lat = lat_vals,
            text = text_vals,
            mode = 'markers',
            # name = ,
            marker = Marker(
                color = "red",
                size = 5,
                symbol = 'circle',
            ))])
    # fig = dict(data = data, layout = layout)
    # py.plot(fig, filename = 'jobs in {}'.format(states[state_abbr.upper()]))


plot_sites_for_state('MI')


