# travel_provider.py

import json
import os
from faker import Faker
from faker.providers import BaseProvider
import random

# Load supported locations from the JSON file
def load_supported_locations():
    base_path = os.path.dirname(__file__)  # Get the directory of the current file
    json_file = os.path.join(base_path, 'supported_locations.json')
    
    with open(json_file, 'r') as f:
        return json.load(f)

supported_locations = load_supported_locations()


class TravelProvider(BaseProvider):
    def __init__(self, faker_instance):
        self.fake = faker_instance  # Use the provided Faker instance

    def flight_lookup(self, departure_city, destination_city, num_options=3):
        """
        Generate a list of flight options between the specified departure and destination cities.
        Validates if the cities are in the supported airports.
        Includes pricing for Economy, Economy+, and Business classes.
        """
        if departure_city not in supported_locations['airports']:
            return {"error": f"Unsupported departure city: {departure_city}. Supported airports are {supported_locations['airports']}"}
        if destination_city not in supported_locations['airports']:
            return {"error": f"Unsupported destination city: {destination_city}. Supported airports are {supported_locations['airports']}"}
        if departure_city == destination_city:
            return {"error": "Departure and destination cities cannot be the same."}
        
        flights = []
        for _ in range(num_options):
            airline = random.choice(['Delta', 'United', 'Southwest', 'JetBlue', 'American Airlines'])
            flight_number = f"{random.choice(['DL', 'UA', 'SW', 'JB', 'AA'])}{random.randint(100, 9999)}"
            departure_time = self.fake.date_time_between(start_date="now", end_date="+30d")
            arrival_time = self.fake.date_time_between(start_date=departure_time, end_date="+30d")

            # Generate random prices for each class
            economy_price = round(random.uniform(100, 300), 2)
            # economy_plus_price = round(random.uniform(200, 400), 2)
            # business_price = round(random.uniform(500, 1000), 2)

            flights.append({
                'airline': airline,
                'departure_airport': departure_city,
                'destination_airport': destination_city,
                'flight_number': flight_number,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'price':  economy_price
            })
        return {"status_code": 200, "flight_options":flights}

    def hotel_lookup(self, city, num_options=3):
        """
        Generate a list of hotel options in the specified city.
        Validates if the city is in the supported hotel cities.
        """
        if city not in supported_locations['hotel_cities']:
            return {"error": f"Unsupported city: {city}. Supported cities are {supported_locations['hotel_cities']}"}

        hotels = []
        for _ in range(num_options):
            hotel_name = random.choice(['Hilton', 'Marriott', 'Hyatt', 'Holiday Inn', 'Sheraton'])
            check_in = self.fake.date_time_between(start_date="now", end_date="+30d")
            check_out = self.fake.date_time_between(start_date=check_in, end_date="+35d")
            price_per_night = random.uniform(100, 500)
            total_price = price_per_night * random.randint(1, 7)  # 1 to 7 nights

            hotels.append({
                'hotel_name': hotel_name,
                'city': city,
                'check_in': check_in,
                'check_out': check_out,
                'price_per_night': round(price_per_night, 2),
                'total_price': round(total_price, 2)
            })
        return hotels

# Initialize Faker globally
fake = Faker()

# Initialize TravelProvider with the Faker instance
travel_provider = TravelProvider(fake)