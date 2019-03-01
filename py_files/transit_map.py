import folium

def get_main_map(boundX, boundY, vehicles, stops):
    main_map = folium.Map(location=[boundX, boundY], zoom_start=6)
    main_map = add_bus_feature_group(main_map, vehicles, stops)
    main_map.save(outfile="templates/map.html")

def add_bus_feature_group(map, buses, stops):
    fg_buses = folium.FeatureGroup(name="Bus locations")
    for row in buses:
        direction = ""
        if row.dir == 1:
            direction = "SOUTH"
        elif row.dir == 2:
            direction = "East"
        elif row.dir == 3:
            direction = "WEST"
        elif row.dir == 4:
            direction = "NORTH"
        information = f'Route: {row.route}\nDirection: {direction}\nBus Number: {row.block}'
        fg_buses.add_child(folium.Marker(location=[row.lat, row.lon], popup=(folium.Popup(information)), icon=folium.Icon(color='blue', icon='bus', prefix='fa')))
    map.add_child(fg_buses)

    fg_stops = folium.FeatureGroup(name="Bus Stops")
    for row in stops:
        name = row.name
        lat = row.lat
        lon = row.lon
        fg_stops.add_child(folium.Marker(location=[lat, lon], popup=folium.Popup(f'Stop Name: {name}'), icon=folium.Icon(color='red', icon_color='white', icon='sign', prefix='fa')))
    map.add_child(fg_stops)

    return map
