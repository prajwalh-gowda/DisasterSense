import pickle
import os

def load_model():
    model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'flood_model.pkl')
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    return model

def predict(model, data):
    prob = model.predict_proba([[
        data['rainfall_mm'],
        data['soil_moisture_pct'],
        data['water_level_cm'],
        data['temp_celsius'],
        data['humidity_pct'],
        data['prev_24h_rain_mm']
    ]])[0][1]

    return prob * 100