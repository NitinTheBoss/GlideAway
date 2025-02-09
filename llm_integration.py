import requests

def setup_ollama():
    """
    Set up Ollama's local API endpoint.
    """
    # Ensure Ollama is running locally (default endpoint: http://localhost:11434)
    ollama_endpoint = "http://localhost:11434/api/generate"
    return ollama_endpoint

def get_best_flight_recommendation(flights):
    """
    Compare the top 5 flights and get the best recommendation from Ollama.
    """
    # Step 1: Prepare the prompt for Ollama
    prompt = (
        f"Here are the top 5 flights from {flights.iloc[0]['DepartingCity']} to {flights.iloc[0]['ArrivingCity']}:\n"
        f"{flights.to_string()}\n"
        "Please compare these flights and recommend the best one based on price, duration, and airline. "
        "Return your response as a JSON object with 'flight_id', 'reason', and 'recommendation'."
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