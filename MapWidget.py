from folium import Map, Marker, Popup, Icon, FeatureGroup, LayerControl, TileLayer
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import *
from os import path

# TODO:  Chloropleth overlays for visited states/countries?
# TODO:  Lines on separate layer for trips, maybe with icons for mode of transportation?


class TravelMap(QWebEngineView):
    def __init__(self, location_data, parent=None):
        super(TravelMap, self).__init__(parent=parent)

        dirname = path.dirname(__file__)
        self.htmlFile = path.join(dirname, 'html/mapTemp.html')

        # tiles: 'cartodbdark_matter', 'cartodbpositron', 'stamentoner', 'mapquestopen', 'openstreetmap'
        mapbox = {'name': 'MapBox Bluish Custom',
                  'link': 'https://api.mapbox.com/styles/v1/atropos158/ckjg82kit6npe1aqsccm9jfrp/tiles/256/{z}/{x}/{y}@2x?' + \
                          'access_token=pk.eyJ1IjoiYXRyb3BvczE1OCIsImEiOiJja2pnNmt3Zjk0OGJhMndwZG82OXk4MTZ3In0.yhQCDJWRZdM8tRHQ26LHoQ',
                  'attr': 'MapBox'}
        carto_light = {'name': 'CartoDB Light',
                       'link': 'cartodbpositron',
                       'attr': 'CartoDB'}
        carto_dark = {'name': 'CartoDB Dark',
                      'link': 'cartodbdark_matter',
                      'attr': 'CartDB'}
        openstreet = {'name': 'OpenStreet Basic',
                      'link': 'openstreetmap',
                      'attr': 'OpenStreet'}
        self.map_styles = [mapbox, carto_light, carto_dark, openstreet]

        self.update_data(location_data)
        # self.layer_ctrl.add_to(self.map)

    def update_data(self, location_data):
        map_obj = self.generate_map(location_data)
        url = self.generate_html(map_obj)
        self.load_map_html(url)
        del map_obj
        # self.show()

    def generate_map(self, locations):
        new_map = Map(location=[0.0, 0.0], zoom_start=2, tiles=None)  # , no_wrap=True, min_zoom=2, max_bounds=True)
        new_map.fit_bounds([[60, -120], [-35, 120]])

        first = True
        for style in self.map_styles:
            if first:
                show = True
            else:
                show = False
            layer = TileLayer(style['link'], name=style['name'], attr=style['attr'], show=show)
            layer.add_to(new_map)

        # dirname = path.dirname(__file__)
        # usa_map = path.join(dirname, 'data/us_states_geo.json')
        # self.map.choropleth(geo_data=usa_map, data=location_data,
        #                    columns=['State', 'Visited'],
        #                    key_on='feature.properties.NAME',
        #                    fill_color='YlGn', fill_opacity=0.6, line_opacity=0.2)
        # self.plot_choropleth(location_data)

        marked_map = self.plot_markers(new_map, locations)

        return marked_map

    def plot_markers(self, map_obj, locations):
        lived_group = FeatureGroup(name='Where I\'ve Lived')
        visit_group = FeatureGroup(name='Where I\'ve Visited')
        wish_group = FeatureGroup(name='Where I Want To Visit')
        other_group = FeatureGroup(name='Other')

        for index, city in locations.iterrows():
            # print(city['coordinates'])
            # print(city['Lived'], city['Visited'], city['Wish'])
            if city['coordinates'] is not None:
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
            # print(latitude, longitude)
            Marker([latitude, longitude], popup=popup, icon=icon_type).add_to(group)

        lived_group.add_to(map_obj)
        visit_group.add_to(map_obj)
        wish_group.add_to(map_obj)
        # other_group.add_to(map_obj)
        LayerControl().add_to(map_obj)

        # self.render()
        return map_obj

    def generate_html(self, map_obj):
        map_obj.save(self.htmlFile)
        return QUrl.fromLocalFile(self.htmlFile)

    def load_map_html(self, url):
        try:
            # As of PyQt6, loading leaflet as QUrl throws js ReferenceError for some reason, so loading as HTML instead.
            #self.page().load(url)
            #self.setUrl(url)
            with open(self.htmlFile, 'r') as f:
                html = f.read()
                self.setHtml(html)
        except:
            print("Cannot load html!")

    # def plot_choropleth(self, locations):
    #     dirname = path.dirname(__file__)
    #     usa_map = path.join(dirname, 'data/us_states_geo.json')
    #     self.map.choropleth(geo_data=usa_map, data=locations,
    #                         columns=['State', 'Visited'],
    #                         key_on='feature.properties.NAME',
    #                         fill_color='YlGn', fill_opacity=0.6, line_opacity=0.2)
    #
    #      LayerControl().add_to(self.map)

