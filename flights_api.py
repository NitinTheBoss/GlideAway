from fastapi import FastAPI, Query
import pandas as pd

app = FastAPI()

# Load dataset
DATA_PATH = "Dataset/flight_data_BOM_BLR.csv"  # Ensure this path matches your file location
df = pd.read_csv(DATA_PATH)

# Standardize column names (just in case)
df.columns = [col.strip().lower() for col in df.columns]

@app.get("/")
def home():
    return {"message": "Flight API is running! Use /flights/ to fetch flight data."}

@app.get("/flights/")
def get_flights(
    origin: str = Query(..., description="Departure city"),
    destination: str = Query(..., description="Arrival city"),
    flight: str = Query(..., description="Flight Name")
):
    """Fetch available flights based on user query"""
    # Ensure columns exist
    required_columns = {"DepartingCity", "ArrivingCity", "FlightName"}
    if not required_columns.issubset(df.columns):
        return {"error": "Dataset does not have required columns: origin, destination, date"}
    
    # Filter dataset
    filtered_flights = df[
        (df["DepartingCity"].str.lower() == origin.lower()) &
        (df["ArrivingCity"].str.lower() == destination.lower()) &
        (df["FlightName"].str.lower() == flight.lower())
    ]
    
    if filtered_flights.empty:
        return {"message": "No flights found for the given route and date."}

    return {"flights": filtered_flights.to_dict(orient="records")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
