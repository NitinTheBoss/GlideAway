from flask import Flask, render_template, request, redirect, url_for
from input_handler import get_user_input
from data_loader import load_dataset
from data_processor import filter_flights
from llm_integration import get_best_flight_recommendation
from data_processor_amadeus import filter_flights_amadeus

app = Flask(__name__)

# Load the dataset
dataset = load_dataset("Dataset/flight_data_BOM_BLR.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input from the form
        source = request.form["source"]
        destination = request.form["destination"]
        date = request.form["date"]
        cheapest_toggle = request.form.get("cheapest_toggle", "off")  # "on" if checked
        direct_toggle = request.form.get("direct_toggle", "off")  # New toggle

        # Filter flights and get the top 5
        # filtered_flights = filter_flights(dataset, source, destination, date, cheapest_toggle, direct_toggle)

        filtered_flights = filter_flights_amadeus(dataset, source, destination, date, cheapest_toggle, direct_toggle)

        if not filtered_flights:
            return render_template("results.html", error="No flights found for the given input.")

        # Get Ollama's recommendation
        recommendation = get_best_flight_recommendation(filtered_flights)

        # Render the results page
        return render_template(
            "results.html",
            flights=filtered_flights.to_dict("records"),
            recommendation=recommendation,
            cheapest_toggle=cheapest_toggle,  # Pass toggle state to results page
            direct_toggle=direct_toggle
        )

    # Render the homepage with the input form
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)