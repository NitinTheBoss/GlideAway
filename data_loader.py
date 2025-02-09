import pandas as pd

def load_dataset(file_path):
    """
    Load the flight dataset from a CSV file.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None