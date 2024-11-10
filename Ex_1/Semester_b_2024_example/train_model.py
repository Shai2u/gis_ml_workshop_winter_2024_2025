import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
import pickle


def model(X_train, y_train, vectorizer = vectorizer, n_estimators = 257, max_depth = 18, min_samples_split = 7):
    def model(X_train, y_train, vectorizer=vectorizer, n_estimators=257, max_depth=18, min_samples_split=7):
        """
        Trains a Random Forest model using the provided training data and hyperparameters, and evaluates its accuracy.

        Parameters
        ----------
        X_train : array-like or sparse matrix of shape (n_samples, n_features)
            The training input samples.
        y_train : array-like of shape (n_samples,)
            The target values (class labels) as integers or strings.
        vectorizer : object, default=vectorizer
            The vectorizer to transform the input data.
        n_estimators : int, default=257
            The number of trees in the forest.
        max_depth : int, default=18
            The maximum depth of the tree.
        min_samples_split : int, default=7
            The minimum number of samples required to split an internal node.

        Returns
        -------
        accuracy : float
            The accuracy of the model on the test data.
        pipeline : sklearn.pipeline.Pipeline
            The trained pipeline containing the vectorizer and the Random Forest classifier.
        """

        # Hyperparameters suggested by Optuna
        n_estimators = n_estimators
        max_depth = max_depth
        min_samples_split = min_samples_split
        vectorizer = vectorizer
        # Random Forest model with suggested hyperparameters
        pipeline = Pipeline([
            ('tfidf', vectorizer),
            ('clf', RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                random_state=42
            ))
        ])

        # Train the model
        pipeline.fit(X_train, y_train)

        # Predict and evaluate
        y_pred = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy, pipeline

def preprocess_data(df):
    """
    Splits the dataframe into training and testing sets.

    Parameters
    ----------
    df : pandas.DataFrame
        The input dataframe containing the data to be split. It must have 
        'text' and 'label' columns where 'text' contains the article content 
        and 'label' contains the target labels (fake/real).

    Returns
    -------
    X_train : pandas.Series
        The training set of the 'text' column.
    X_test : pandas.Series
        The testing set of the 'text' column.
    y_train : pandas.Series
        The training set of the 'label' column.
    y_test : pandas.Series
        The testing set of the 'label' column.
    """
    X = df['text']  # Use 'text' column for the article content
    y = df['label']  # Use 'label' column for the target (fake/real)
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

def main(file_path):
    """
    Main function to read data, preprocess it, and train a model.

    Parameters
    ----------
    file_path : str
        The path to the CSV file containing the dataset.

    Returns
    -------
    model_pipeline : sklearn.pipeline.Pipeline
        The trained model pipeline.
    """
    df = pd.read_csv(file_path)

    X_train, X_test, y_train, y_test = preprocess_data(df)
    # Step 4: Vectorization using TF-IDF
    vectorizer = TfidfVectorizer(max_features=10000, stop_words='english')
    accuracy, model_pipeline = model(X_train, y_train, vectorizer)
    print(f'Accuracy: {accuracy}')
    return model_pipeline

if __name__ == "__main__":
    file_path = '../../data/Combined.csv'
    model_pipeline = main(file_path)
    # Saving the pipeline
    with open('model.pkl', 'wb') as file:
        pickle.dump(model_pipeline, file)
     


