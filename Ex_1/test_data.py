import pickle
import pandas as pd
from sklearn.model_selection import train_test_split

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

    sample = df.sample(1000)
    X = sample['text']  # Use 'text' column for the article content
    y = sample['label']  # Use 'label' column for the target (fake/real)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    result = model.predict([X_train.iloc[0]])
