from input_handler import get_user_input
from data_loader import load_dataset
from data_processor import filter_flights
from llm_integration import get_best_flight_recommendation

def main():
    # Step 1: Get user input
    source, destination, date = get_user_input()

    # Step 2: Load dataset
    dataset = load_dataset("Dataset/flight_data_BOM_BLR.csv")  # Replace with your dataset path
    if dataset is None:
        return

    # Step 3: Filter flights and select the top 5
    filtered_flights = filter_flights(dataset, source, destination, date)
    if filtered_flights.empty:
        print("No flights found for the given input.")
        return

    # Step 4: Get best flight recommendation
    recommendation = get_best_flight_recommendation(filtered_flights)

if __name__ == "__main__":
    main()