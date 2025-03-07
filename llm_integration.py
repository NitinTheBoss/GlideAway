import requests

def setup_ollama():
    """
    Set up Ollama's local API endpoint.
    """
    # Ensure Ollama is running locally (default endpoint: http://localhost:11434)
    ollama_endpoint = "http://localhost:11434/api/generate"
    return ollama_endpoint

def get_best_flight_recommendation(flights, cheapest_toggle, direct_toggle):
    """
    Compare the top 5 flights and get the best recommendation from Ollama.
    """
    # Step 1: Prepare the prompt for Ollama
    prompt = (
        f"Here are the flights from {flights.iloc[0]['departure_airport']} to "
        f"{flights.iloc[0]['arrival_airport']}:\n"
        f"{flights.to_string()}\n"
        "Select the best flight. "
    )

    if direct_toggle:
        prompt = prompt + "Prefer direct flights. "
    if cheapest_toggle:
        prompt = prompt + "Prefer cheapest flights options. "

    prompt = prompt + ("Give me the recommendation with "
                        "'Flight ID:'"
                        "'Price:'"
                        "'Airline'"
                        "'Departure Time:'"
                        "'Duration:'"
                        "'Reason:'"
                       )

    # Step 2: Send the prompt to Ollama
    ollama_endpoint = setup_ollama()
    response = requests.post(
        ollama_endpoint,
        json={
            "model": "llama3.2",  # Replace with your preferred model (e.g., llama3, gemma)
            "prompt": prompt,
            "stream": False,  # Set to True if you want streaming responses
        },
    )

    # Step 3: Parse the response
    if response.status_code == 200:
        recommendation = response.json()["response"]
        print("\nOllama's Recommendation:")
        print(recommendation)
        return recommendation
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None