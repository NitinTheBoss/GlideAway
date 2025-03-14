from flask import Flask, render_template, request
from llm_integration import get_best_flight_recommendation
from data_processor_amadeus import filter_flights_amadeus

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input from the form
        source = request.form["source"]
        destination = request.form["destination"]
        date = request.form["date"]
        cheapest_toggle = request.form.get("cheapest_toggle", "off")  # "on" if checked
        direct_toggle = request.form.get("direct_toggle", "off")  # New toggle

        filtered_flights = filter_flights_amadeus(source, destination, date)

        if filtered_flights.empty:
            return render_template("results.html", error="No flights found for the given input.")

        # Get Gemini's recommendation
        recommendation = get_best_flight_recommendation(filtered_flights, cheapest_toggle, direct_toggle)

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

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)