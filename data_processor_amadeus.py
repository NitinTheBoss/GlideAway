import requests

# Your API credentials
API_KEY = "Replace_from_whatsapp"
API_SECRET = "Replace_from_whatsapp"

# Amadeus API URLs
TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHT_SEARCH_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"


# Function to get access token
def get_access_token():
    payload = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": API_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(TOKEN_URL, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Failed to get access token:", response.text)
        return None


# Function to search flights
def search_flights(access_token, origin, destination, date, max_price=500):
    headers = {"Authorization": f"Bearer {access_token}"}
    search_params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": 1,
        "currencyCode": "USD",
        "maxPrice": max_price  # Filters flights less than $200
    }

    response = requests.get(FLIGHT_SEARCH_URL, headers=headers, params=search_params)

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print("Error:", response.status_code, response.text)
        return []


# Function to format and display flight details
def print_flight_details(flights):
    if not flights:
        print("No flights found under $200.")
        return

    print("\nAvailable Flights (Under $200):\n" + "-" * 50)
    for flight in flights:
        price = flight["price"]["total"]
        itinerary = flight["itineraries"][0]["segments"][0]  # First segment

        airline = itinerary["carrierCode"]
        departure_airport = itinerary["departure"]["iataCode"]
        arrival_airport = itinerary["arrival"]["iataCode"]
        departure_time = itinerary["departure"]["at"]
        arrival_time = itinerary["arrival"]["at"]

        print(f"Airline: {airline}")
        print(f"From: {departure_airport} -> {arrival_airport}")
        print(f"Departure: {departure_time}")
        print(f"Arrival: {arrival_time}")
        print(f"Price: ${price}")
        print("-" * 50)


def filter_flights_amadeus(data, source, destination, date, cheapest_toggle, direct_toggle):
    """
    Filter flights based on user input (source, destination, date).
    Sort by price if "Cheapest Flight" toggle is on.
    """
    # Convert the 'date' column to datetime (if not already)
    # data['date'] = pd.to_datetime(data['date']).dt.date

    # Filter flights by source, destination, and date
    access_token = get_access_token()

    if access_token:
        flights = search_flights(access_token, source, destination, date)
        print_flight_details(flights)

        return flights