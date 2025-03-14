import os
from google import genai
from google.genai import types

# Load API keys from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def setup_gemini(api_key=None):
    """
    Set up Gemini API client with explicit API key handling.

    Args:
        api_key: Optional explicit API key. If None, will try to get from environment.
    """
    api_key = api_key or GEMINI_API_KEY
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY. Set it as an environment variable.")

    client = genai.Client(api_key=api_key)
    return client


def get_best_flight_recommendation(flights, cheapest_toggle, direct_toggle, api_key=None):
    """
    Compare the top 5 flights and get the best recommendation from Gemini.

    Args:
        flights: DataFrame containing flight information
        cheapest_toggle: Boolean indicating preference for cheapest flights
        direct_toggle: Boolean indicating preference for direct flights
        api_key: Optional Gemini API key
    """
    prompt = (
        f"Here are the flights from {flights.iloc[0]['departure_airport']} to "
        f"{flights.iloc[0]['arrival_airport']}:\n"
        f"{flights.to_string()}\n"
        "Select the best flight. "
    )
    if direct_toggle:
        prompt += "Prefer direct flights. "
    if cheapest_toggle:
        prompt += "Prefer cheapest flights options. "
    prompt += ("Give me the recommendation with "
               "'Flight ID:'"
               "'Price:'"
               "'Airline' "
               "'Departure Time:'"
               "'Duration:'"
               "'Reason:'"
               )

    try:
        client = setup_gemini(api_key)
        model = "gemini-2.0-flash"

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                ],
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature=0.7,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="text/plain",
        )

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )

        recommendation = response.text
        print("\nGemini's Recommendation:")
        print(recommendation)
        return recommendation
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Unable to get flight recommendation. Error: {str(e)}"