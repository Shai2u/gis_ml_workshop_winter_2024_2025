import pickle
import pandas as pd

def load_model(file_path):
    with open(file_path, 'rb') as file:
        model = pickle.load(file)
    return model

# Example usage
# model = load_model('path_to_your_model.pkl')

if __name__ == "__main__":
    file_path = '../../data/Combined_with_lat_long_trf_3.csv'
    df = pd.read_csv(file_path)
    model = load_model('model.pkl')
