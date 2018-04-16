    data = Data([ Scattermapbox(
        title = 'Software Jobs in America',
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
    