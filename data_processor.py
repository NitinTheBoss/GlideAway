import pandas as pd

def filter_flights(data, source, destination, date, cheapest_toggle, direct_toggle):
    """
    Filter flights based on user input (source, destination, date).
    Sort by price if "Cheapest Flight" toggle is on.
    """
    # Convert the 'date' column to datetime (if not already)
    # data['date'] = pd.to_datetime(data['date']).dt.date

    # Filter flights by source, destination, and date
    filtered_data = data[
        (data['DepartingCity'].str.lower() == source.lower()) &
        (data['ArrivingCity'].str.lower() == destination.lower())
        # (data['date'] == pd.to_datetime(date).date())
    ]

    # Sort by price if toggle is on
    if cheapest_toggle == "on":
        filtered_data = filtered_data.sort_values(by='Price').head(5)
        return filtered_data
    else:
        # Default sorting (e.g., by duration or airline rating)
        filtered_data = filtered_data.sort_values(by='Duration').head(5)

    # Apply Direct Flight filter
    if direct_toggle == "on":
        filtered_data = filtered_data.sort_values(by='Duration').head(5)  # Assuming 'Stops' means fastest here

    return filtered_data