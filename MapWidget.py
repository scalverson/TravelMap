from folium import Map, Marker, Popup, Icon, FeatureGroup, LayerControl, TileLayer
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import *
from os import path


class TravelMap(QWebEngineView):
    def __init__(self, location_data):
        super(TravelMap, self).__init__()

        # tiles: 'cartodbdark_matter', 'cartodbpositron', 'stamentoner', 'mapquestopen', 'openstreetmap'
        self.map = Map(location=[0.0, 0.0], zoom_start=2, tiles='cartodbpositron')
        self.map.fit_bounds([[60, -120], [-35, 120]])
        TileLayer('openstreetmap').add_to(self.map)
        #TileLayer('mapquestopen').add_to(self.map)
        TileLayer('cartodbpositron').add_to(self.map)
        TileLayer('cartodbdark_matter').add_to(self.map)
        #TileLayer('stamentoner').add_to(self.map)

        #dirname = path.dirname(__file__)
        #usa_map = path.join(dirname, 'data/us_states_geo.json')
        #self.map.choropleth(geo_data=usa_map, data=location_data,
        #                    columns=['State', 'Visited'],
        #                    key_on='feature.properties.NAME',
        #                    fill_color='YlGn', fill_opacity=0.6, line_opacity=0.2)

        #self.plot_choropleth(location_data)
        self.plot_markers(location_data)

        dirname = path.dirname(__file__)
        htmlFile = path.join(dirname, 'html/mapTemp.html')
        self.map.save(htmlFile)
        self.url = QUrl.fromLocalFile(htmlFile)

        self.load(self.url)
        self.show()

    def update_data(self):
        pass

    def plot_markers(self, locations):
        lived_group = FeatureGroup(name='Where I\'ve Lived')
        visit_group = FeatureGroup(name='Where I\'ve Visited')
        wish_group = FeatureGroup(name='Where I Want To Visit')
        other_group = FeatureGroup(name='Other')

        for index, city in locations.iterrows():
            # print(city['coordinates'])
            if city['coordinates'] is not None:
                # print(icon_type)
                if city['Lived']:
                    icon_type = Icon(color='darkgreen', icon_color='darkred', icon='home')
                    group = lived_group
                elif city['Favorite']:
                    icon_type = Icon(color='darkblue', icon_color='orange', icon='star')
                    group = visit_group
                elif city['Visited']:
                    icon_type = Icon(color='darkblue', icon_color='orange', icon='ok')
                    group = visit_group
                elif city['Wish']:
                    # print(city['coordinates'])
                    icon_type = Icon(color='lightblue', icon_color='cadetblue', icon='list-alt')
                    group = wish_group
                else:
                    icon_type = Icon()
                    group = other_group
                # print(icon_type)
                # icon_type = Icon(color='green', icon='home')
                popup = Popup(city["Full Name"], parse_html=True)
                coords = city['coordinates'].replace('(', '').split(',')
                try:
                    latitude = float(coords[0])
                    longitude = float(coords[1])
                except ValueError:
                    print(city['City'] + ' type error for coordinates: ' + city['coordinates'])
                    continue
                #print(latitude, longitude)
                Marker([latitude, longitude], popup=popup, icon=icon_type).add_to(group)

        lived_group.add_to(self.map)
        visit_group.add_to(self.map)
        wish_group.add_to(self.map)
        # other_group.add_to(self.map)
        LayerControl().add_to(self.map)

        #self.render()

    def plot_choropleth(self, locations):
        dirname = path.dirname(__file__)
        usa_map = path.join(dirname, 'data/us_states_geo.json')
        self.map.choropleth(geo_data=usa_map, data=locations,
                       columns=['State', 'Visited'],
                       key_on='feature.properties.NAME',
                       fill_color='YlGn', fill_opacity=0.6, line_opacity=0.2)

        #LayerControl().add_to(self.map)

