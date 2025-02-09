import pandas as pd

def filter_flights(data, source, destination, date):
    """
    Filter flights based on user input (source, destination, and date).
    Select the top 5 flights based on price.
    """
    # # Convert the 'date' column to datetime (if not already)
    # data['date'] = pd.to_datetime(data['date']).dt.date

    # Filter flights by source, destination, and date
    filtered_data = data[
        (data['DepartingCity'].str.lower() == source.lower()) &
        (data['ArrivingCity'].str.lower() == destination.lower())
    ]

    # Sort by price and select the top 5 flights
    top_5_flights = filtered_data.sort_values(by='Price').head(5)
    return top_5_flights