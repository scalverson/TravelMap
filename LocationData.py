import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


class LocationHandler(object):
    def __init__(self):
        super(LocationHandler, self).__init__()

        self.geocode_delay = 0.2  # seconds
        self.data = GeoData().data

    def read_csv(self, file):
        csv_data = pd.read_csv(file, na_values="")
        csv_data["State"] = " " + csv_data["State"]
        csv_data.fillna("", inplace=True)

        self.data = pd.concat([self.data, csv_data], sort=False)
        #print(self.data)

        #for index, city in self.data.iterrows():
        #    if not city['Latitude'] or not city['Longitude']:
        #        #print(city)
        #        self.data['Latitude'][index], self.data['Longitude'][index] = self.get_geoloc(self.format_name(city))
        #print(self.data['Latitude'])

    def write_csv(self, file_name=''):
        self.data.to_csv(file_name, index=False)

    def new_location(self, city=''):
        if city:
            pass

    def format_name(self, city=pd.DataFrame):
        city["State"] = " " + city["State"]
        name_str = city["Address"].map(str) + " " + city["City"].map(str) + city["State"] + ", " + city["Country"]
        return name_str

    def get_geoloc(self, city):
        if city is not None:
            geolocator = Nominatim(user_agent="My_App")
            geocode = RateLimiter(geolocator.geocode, min_delay_seconds=self.geocode_delay)
            address, (lat, long) = geolocator.geocode(city)
            print(lat, long)
            return [lat, long]


class GeoData(object):
    def __init__(self):
        super(GeoData, self).__init__()

        self.data = pd.DataFrame(columns=['Address', 'City', 'State', 'Country', 'Visited', 'Lived', 'Wish',
                                          'Favorite', 'Full Name', 'geocode', 'coordinates'])

    def add_entry(self, data=pd.DataFrame):
        self.data = pd.concat([self.data, data], sort=False).fillna("", inplace=True)

    @property
    def full_name(self, city=pd.DataFrame):
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



