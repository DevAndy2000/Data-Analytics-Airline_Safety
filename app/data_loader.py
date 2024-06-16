import pandas as pd

def load_data():
    file_path = 'data/airplane_safety_data.csv'  # Make sure this path is correct
    data = pd.read_csv(file_path)
    return data