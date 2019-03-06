import folium
from bs4 import BeautifulSoup as Soup

def get_main_map(boundX, boundY, vehicles):
    map = folium.Map(location=[boundX, boundY], zoom_start=12)
    map = add_bus_feature_group(map, vehicles)
    map.save('templates/map.html')
    html = """
        <form method="GET" action="/">
        <button type="submit">
            Back to home
        </button>
        </form>
        """
    with open("templates/map.html") as f:
        soup = Soup(f)
    map_html = soup.find('div')
    soup.div.insert_before(html)

    return map

def add_bus_feature_group(map, buses):
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
        route = row.route
        bus = row.block
        information = f'Route:{route}\nDirection:{direction}\nBus Number:{bus}'
        folium.Marker(location=[row.lat, row.lon], popup=(folium.Popup(information)), icon=folium.Icon(color='blue', icon_color='white', icon='bus', prefix='fa')).add_to(map)
    return map
