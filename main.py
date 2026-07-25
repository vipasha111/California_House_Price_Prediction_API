
import io
import joblib 
import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

import os
print(__file__)

app = FastAPI(
    title="California Housing Price Prediction API",
    description="This API predicts the price of houses in California based on various features using a trained Random Forest Regressor model.",
    version="1.0.0"
)

model = joblib.load("house_model.joblib")
features = joblib.load("house_features.joblib")


#inputs schema
class HouseFeatures(BaseModel):
    MedInc: float = Field(gt = 0, description="Median income of Neighborhood")
    HouseAge: float = Field(gt = 0, description="Average age of house in the block")
    AveRooms: float = Field(gt = 0, description="Average number of rooms per household")
    AveBedrms: float = Field(gt = 0, description="Average number of bedrooms per household")
    Population: float = Field(gt = 0, description="Population of the block")    
    AveOccup: float = Field(gt = 0, description="Average number of household members")
    Latitude: float = Field(ge = 32.5, le = 42.5, description="Latitude of the block")
    Longitude: float = Field(ge = -124.5, le = -114.5, description="Longitude of the block")

    #home
@app.get("/")
def home():
    return {"message": "Welcome to the California Housing Price Prediction API!",
            "status": "API is running successfully.",
            "endpoints": "send POST request to /predict"}

@app.get("/health")
def health_check():
    return {
        "status": "API is running successfully.",
        "model": "Random Forest Regressor",
        "features": features,
        "avg_error": "$39,000"
        }


#prediction
@app.post("/predict")
def predict_price(house: HouseFeatures):
    try:
        input_data = pd.DataFrame([{
            "MedInc": house.MedInc,
            "HouseAge": house.HouseAge,
            "AveRooms": house.AveRooms,
            "AveBedrms": house.AveBedrms,
            "Population": house.Population,
            "AveOccup": house.AveOccup,
            "Latitude": house.Latitude,
            "Longitude": house.Longitude
        }])

        predicted = model.predict(input_data)[0]
        price_usd = predicted * 100000

        return {"predicted_price": f"${price_usd:,.0f}",
                "predicted_price_short": f"${predicted:.2f} hundred thousands",
                "confidence_range": f"${price_usd - 39000:,.0f} to ${price_usd + 39000:,.0f}"}

    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"prediction failed: {str(e)}"
        )
    
@app.post("/predict_csv")
async def predict_file(file: UploadFile = File(...)):   
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

    contents = await file.read()
    #b'name,age,city\nAlice,30,New York\nBob,25,Los Angeles\nCharlie,35,Chicago\n'

    df = pd.read_csv(io.BytesIO(contents))

    required_columns = [
        'MedInc', 'HouseAge', 'AveRooms', 'AveBedrms',
        'Population', 'AveOccup', 'Latitude', 'Longitude'
    ]

    missing_columns = [
        col for col in required_columns 
        if col not in df.columns
        ]

    if missing_columns:
        raise HTTPException(
            status_code=400, 
            detail=f"Missing required columns: {', '.join(missing_columns)}"
        )

    try:
        predictions = model.predict(df[required_columns])
        df['PredictedPrice'] = predictions * 100000
        df['PredictedPrice'] = df["PredictedPrice"].apply(lambda x: f"${x:,.0f}")

        output = df.to_csv(index=False)
        
        

        return StreamingResponse(
            io.StringIO(output),
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=predictions.csv"
                }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )