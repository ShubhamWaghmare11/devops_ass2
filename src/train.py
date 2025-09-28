import mlflow
from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle

data = pd.read_csv('data/data.csv')

X = data.drop('Price', axis=1)
y = data['Price']

x_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_experiment("LinearRegression")

model = LinearRegression()

with mlflow.start_run():
    model.fit(x_train, y_train)
    y_pred = model.predict(X_test)
    with open("linear_regression_model.pkl", "wb") as f:
        pickle.dump(model, f)
    feature_columns = X.columns.tolist()
    with open("features.pkl", "wb") as f:
        pickle.dump(feature_columns, f)

    mse = mean_squared_error(y_test, y_pred)
    mlflow.sklearn.log_model(model, "linear_regression_model")
    mlflow.log_metric("mse", mse)
    mlflow.log_param("random_state", 42)
    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_param("train_size", len(x_train))
    mlflow.log_param("test_size", len(X_test))
    mlflow.log_metric("train_score", model.score(x_train, y_train))
    mlflow.log_metric("test_score", model.score(X_test, y_test))
    mlflow.log_param("learning_rate", 1)
    mlflow.log_param("epochs", 1) 
    mlflow.sklearn.log_model(model, "linear_regression_model")
    print("Model training complete and logged to MLflow.")    