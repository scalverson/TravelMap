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

db_fields = ['Address', 'City', 'State', 'Country', 'Visited', 'Lived', 'Wish', 'Favorite', 'Full Name',
             'geocode', 'coordinates']


class LocationHandler(object):
    def __init__(self):
        super(LocationHandler, self).__init__()

        self.geocode_delay = 0.2  # seconds
        self.database = GeoData()
        self.data = self.database.data

    def read_csv(self, file):
        csv_data = pd.read_csv(file, na_values="")
        csv_data["State"] = " " + csv_data["State"]
        csv_data.fillna("", inplace=True)

        self.data = pd.concat([self.data, csv_data], sort=False)
        #print(self.data)

        for index, city in self.data.iterrows():
            if not city['coordinates']:
                print(city)
                address, lat, long = self.get_geoloc(self.format_name(city))
                city['geocode'] = address
                city['coordinates'] = (lat, long, 0)
        #print(self.data['Latitude'])

    def write_csv(self, file_name=''):
        self.data.to_csv(file_name, index=False)

    def new_location(self, address='', city='', state='', country=''):
        location = pd.DataFrame(columns=db_fields)
        location['Address'] = address
        location['City'] = city
        location['State'] = state
        location['Country'] = country
        location['Full Name'] = self.format_name(location)
        address, lat, long = self.get_geoloc(location['Full Name'])
        location['geocode'] = address
        location['coordinates'] = (lat, long, 0)
        self.database.add_entry(location)

    def format_name(self, city=pd.DataFrame()):
        name_str = ''
        if not city.empty:
            city["State"] = " " + city["State"]
            name_str = city["Address"].map(str) + " " + city["City"].map(str) + city["State"] + ", " + city["Country"]
        return name_str

    def get_geoloc(self, city=''):
        if city:
            geo_locator = Nominatim(user_agent="My_App")
            geocode = RateLimiter(geo_locator.geocode, min_delay_seconds=self.geocode_delay)
            address, (lat, long) = geo_locator.geocode(city)
            print(lat, long)
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


class GeoData(object):
    def __init__(self):
        super(GeoData, self).__init__()

        self.data = pd.DataFrame(columns=db_fields)

    def add_entry(self, data=pd.DataFrame()):
        if not data.empty:
            self.data = pd.concat([self.data, data], sort=False).fillna("", inplace=True)

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

