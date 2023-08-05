import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
def load_data(filepath):
    data = pd.read_csv(filepath)
    print(data.head())
    return data

def preprocess_data(data):
    """
    Preprocess the data, including feature engineering and scaling.
    """
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    return scaled_data

def split_data(data):
    """
    Split the data into training and testing sets.
    """
    X = data[:, 1:]
    y = data[:, :1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    """
    Train a Random Forest Regressor model to predict levels of alpha, beta, theta, and delta.
    """
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def predict_levels(model, X_test):
    """
    Predict the levels of alpha, beta, theta, and delta for a particular point.
    """
    y_pred = model.predict(X_test)
    return y_pred

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the performance of the model on the test set.
    """
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    print(f"R2 Score: {r2}")



def visualize_predictions(model, X_test, y_test):
    """
    Visualize the predicted and actual levels of alpha, beta, theta, and delta.
    """
    X_test= X_test[:-3]
    y_test = y_test[:-3]
    y_pred = predict_levels(model, X_test)

    y_test = y_test.reshape(-1, 4)
    y_pred = y_pred.reshape(-1, 4)


    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

   
    axs[0, 0].set_title("Alpha")
    axs[0, 1].set_title("Beta")
    axs[1, 0].set_title("Theta")
    axs[1, 1].set_title("Delta")

    axs[0, 0].plot(y_test[:, 0], label="Actual")
    axs[0, 0].plot(y_pred[:, 0], label="Predicted")
    axs[0, 1].plot(y_test[:, 1], label="Actual")
    axs[0, 1].plot(y_pred[:, 1], label="Predicted")
    axs[1, 0].plot(y_test[:, 2], label="Actual")
    axs[1, 0].plot(y_pred[:, 2], label="Predicted")
    axs[1, 1].plot(y_test[:, 3], label="Actual")
    axs[1, 1].plot(y_pred[:, 3], label="Predicted")

    
    axs[0, 0].legend()
    axs[0, 1].legend()
    axs[1, 0].legend()
    axs[1, 1].legend()

    plt.show()

