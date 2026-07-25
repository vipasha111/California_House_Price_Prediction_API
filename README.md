# 🏠 California House Price Prediction API

A Machine Learning-based REST API that predicts California house prices using a trained **Random Forest Regressor**. The model is deployed using **FastAPI** and supports both individual house-price predictions and batch predictions through CSV files.

## 📌 Project Overview

House price estimation often requires analyzing multiple factors such as location, income, house age, number of rooms, and population.

This project provides an automated, data-driven approach to estimate house prices using Machine Learning.

The API accepts housing-related features and returns an estimated house price.

---

## 🎯 Objectives

- Build a Machine Learning model for California house-price prediction.
- Use a Random Forest Regressor for prediction.
- Save and load the trained model using Joblib.
- Deploy the model using FastAPI.
- Provide an API for individual house-price predictions.
- Support batch predictions using CSV files.
- Validate user inputs using Pydantic.

---

## 🧠 Machine Learning Model

The project uses a **Random Forest Regressor** trained on the California Housing dataset.

### Input Features

| Feature | Description |
|---|---|
| `MedInc` | Median income of the neighborhood |
| `HouseAge` | Average age of houses in the block |
| `AveRooms` | Average number of rooms per household |
| `AveBedrms` | Average number of bedrooms per household |
| `Population` | Population of the block |
| `AveOccup` | Average number of household members |
| `Latitude` | Latitude of the block |
| `Longitude` | Longitude of the block |

The model predicts the median house value, which is converted into an estimated dollar price.

---

## 🚀 Key Features

### 🔹 Individual Prediction

Predict the estimated price of a house by providing its features through the `/predict` endpoint.

### 🔹 Batch Prediction

Upload a CSV containing multiple properties through `/predict_csv` and receive a CSV containing predicted prices.

### 🔹 Input Validation

Pydantic is used to validate incoming data and ensure that values fall within appropriate ranges.

### 🔹 REST API

The trained Machine Learning model is exposed through a FastAPI REST API, making it easy to integrate with other applications.

### 🔹 Interactive Documentation

FastAPI automatically generates interactive Swagger documentation, allowing users to test the API directly from the browser.

---

## 🏡 How It Improves House Price Estimation

Traditional property price estimation can involve manual research, comparisons, and consultation with real-estate professionals.

This project provides a **fast, automated, and data-driven preliminary estimation system**.

It can:

- ⚡ Generate predictions within seconds.
- 📊 Analyze multiple housing and geographic features simultaneously.
- 🤖 Provide consistent, data-driven estimates.
- 📁 Process multiple properties through CSV batch prediction.
- 🔌 Be integrated into websites, dashboards, or other applications.
- 💰 Reduce repeated manual calculations during initial property evaluation.
- 📈 Be retrained using newer datasets to improve its usefulness over time.

The system can work as a **first-level price estimation tool**, helping buyers, sellers, and property platforms make faster and more informed decisions before detailed professional evaluation.

---

## ⚙️ API Endpoints

### `GET /`

Returns a welcome message and basic API information.

### `GET /health`

Checks whether the API is running and provides information about the loaded model and features.

### `POST /predict`

Predicts the price of a single house.

#### Example Input

```json
{
    "MedInc": 8.3,
    "HouseAge": 20,
    "AveRooms": 6.0,
    "AveBedrms": 1.0,
    "Population": 500,
    "AveOccup": 2.5,
    "Latitude": 34.05,
    "Longitude": -118.25
}

### EXample response
{
    "predicted_price": "$XXX,XXX",
    "predicted_price_short": "$X.XX hundred thousands",
    "confidence_range": "$XXX,XXX to $XXX,XXX"
}
