from PyQt5.QtCore import pyqtSignal, QObject
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from pycountry import countries

states = ['Alaska', 'Alabama', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida',
          'Georgia', 'Hawaii', 'Idaho', 'Indiana', 'Illinois', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
          'Maryland', 'Massachusetts', 'Michigan', 'Mississippi', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
          'New Jersey', 'New Mexico', 'New York', 'Minnesota', 'Missouri', 'North Carolina', 'North Dakota',
          'Oklahoma', 'Ohio', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee',
          'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

db_fields = ['Address', 'City', 'State', 'Country', 'Visited', 'Lived', 'Wish', 'Favorite', 'Full Name', 'geocode', 'coordinates']


class LocationHandler(QObject):
    updated = pyqtSignal()
    data_changed = pyqtSignal()

    def __init__(self):
        super(LocationHandler, self).__init__()

        self.geocode_delay = 0.2  # seconds
        self.database = GeoData()

        self.saved = True

        self.database.entry_added.connect(self.on_data_change)

    @property
    def saved(self):
        return self._saved

    @saved.setter
    def saved(self, state=False):
        self.data_changed.emit()
        self._saved = state

    def on_data_change(self, data=pd.DataFrame):
        if not data.empty:
            self.saved = False
            self.updated.emit()

    @property
    def data(self):
        return self.database.data

    def read_csv(self, file):
        data = pd.read_csv(file, na_values="")
        data["State"] = " " + data["State"]
        data.fillna("", inplace=True)

        # data = pd.concat([self.data, csv_data], sort=False)
        # self.database.add_entry(csv_data)

        # Retrieve geo data for entries lacking it
        for index, city in data[data['coordinates'] == ''].iterrows():
            if city['Full Name']:
                full_name = city['Full Name']
            else:
                full_name = self.format_name(city)
                data.at[index, 'Full Name'] = full_name
            address, lat, long = self.get_geoloc(full_name)
            data.at[index, 'geocode'] = address
            data.at[index, 'coordinates'] = '(' + str(lat) + ' ,' + str(long) + ', 0)'

        self.database.add_entry(data)
        self.saved = True

    def write_csv(self, file_name=''):
        self.data.to_csv(file_name, index=False)
        self.saved = True

    def new_location(self, loc_data):  # address='', city='', state='', country=''):
        loc_in_data = self.data[(self.data['Address'] == loc_data['Address']) &
                                (self.data['City'] == loc_data['City']) &
                                (self.data['State'] == loc_data['State']) &
                                (self.data['Country'] == loc_data['Country'])]
        if not loc_in_data.empty:
            ind = loc_in_data.index
            for key in loc_data.keys():
                self.database.data.at[ind, key] = loc_data[key]
            self.on_data_change(self.data.loc[ind])
        else:
            location = pd.DataFrame(columns=db_fields)
            if 'Address' in loc_data.keys():
                location.at[0, 'Address'] = loc_data['Address']
            if 'City' in loc_data.keys():
                location.at[0, 'City'] = loc_data['City']
            if 'State' in loc_data.keys():
                location.at[0, 'State'] = loc_data['State']
            if 'Country' in loc_data.keys():
                location.at[0, 'Country'] = loc_data['Country']
            if 'Lived' in loc_data.keys():
                location.at[0, 'Lived'] = loc_data['Lived']
            if 'Visited' in loc_data.keys():
                location.at[0, 'Visited'] = loc_data['Visited']
            if 'Wish' in loc_data.keys():
                location.at[0, 'Wish'] = loc_data['Wish']
            if 'Favorite' in loc_data.keys():
                location.at[0, 'Favorite'] = loc_data['Favorite']
            full_name = self.format_name(location.loc[0])
            location.at[0, 'Full Name'] = full_name
            address, lat, long = self.get_geoloc(full_name)
            location.at[0, 'geocode'] = address
            if lat is not None and long is not None:
                location.at[0, 'coordinates'] = '(' + str(lat) + ' ,' + str(long) + ' , 0)'
            self.database.add_entry(location)

    def format_name(self, city=pd.DataFrame()):
        name_str = ''
        if not city.empty:
            city["State"] = " " + city["State"]
            name_str = city["Address"] + " " + city["City"] + city["State"] + ", " + city["Country"]
        return name_str

    def get_geoloc(self, city=''):
        address = ''
        lat = None
        long = None
        if city:
            geo_locator = Nominatim(user_agent="My_App")
            geocode = RateLimiter(geo_locator.geocode, min_delay_seconds=self.geocode_delay)
            try:
                address, (lat, long) = geo_locator.geocode(city)
            except TypeError:
                print('Could not retrieve geocode!  Check input fields and try again.')
            # print(address, lat, long)
        return address, lat, long

    @property
    def total_countries(self):
        return len(countries)

    @property
    def total_states(self):
        return len(states)

    @property
    def visited_states(self):
        state_list = []
        for index, entry in self.data.iterrows():
            if entry['Visited'] is True and entry['State']:
                state_list.append(entry['State'])
        return list(set(state_list))

    @property
    def visited_countries(self):
        country_list = []
        for index, entry in self.data.iterrows():
            if entry['Visited'] is True and entry['Country']:
                country_list.append(entry['Country'])
        return list(set(country_list))

    @property
    def country_cnt(self):
        return len(self.visited_countries)

    @property
    def state_cnt(self):
        return len(self.visited_states)

    @property
    def location_cnt(self):
        return len(self.data.index)


class GeoData(QObject):
    entry_added = pyqtSignal(pd.DataFrame)

    def __init__(self):
        super(GeoData, self).__init__()

        self.data = pd.DataFrame(columns=db_fields)

    def add_entry(self, data):
        # print(data)
        self.data = self.data.append(data, sort=False, ignore_index=True)
        # print(self.data)
        self.entry_added.emit(data)

    @property
    def full_name(self, city=pd.DataFrame()):
        city["State"] = " " + city["State"]
        return city["Address"] + " " + city["City"] + city["State"] + ", " + city["Country"]

    @property
    def coords(self, city_str=''):
        if not city_str:
            print('Must enter city.')
            return
        else:
            city = self.data['City'].index(city_str)
            if city is not None:
                coord_str = city['coordinates'].replace('(', '').split(',')
                try:
                    latitude = float(coord_str[0])
                    longitude = float(coord_str[1])
                except ValueError:
                    print(city['City'] + ' type error for coordinates: ' + city['coordinates'])
                    return
                return [latitude, longitude]
            else:
                print('No instances of ' + city_str + ' found.')
                return

