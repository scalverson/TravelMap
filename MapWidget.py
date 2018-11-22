from folium import Map, Marker, Popup, Icon, FeatureGroup, LayerControl


class TravelMap(Map)
    def __init__(self):
        super().__init__(location=[0.0, 0.0], zoom_start = 2)

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
                    icon_type = folium.Icon()
                    group = other_group
                # print(icon_type)
                # icon_type = Icon(color='green', icon='home')
                popup = Popup(city["Full Name"], parse_html=True)
                Marker([city['coordinates'][0], city['coordinates'][1]],
                              popup=popup,
                              icon=icon_type,
                              ).add_to(group)

        lived_group.add_to(self)
        visit_group.add_to(self)
        wish_group.add_to(self)
        # other_group.add_to(self)
        LayerControl().add_to(self)

        self.render()