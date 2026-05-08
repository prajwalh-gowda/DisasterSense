import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle, os

np.random.seed(42)
n = 2000

data = {
    'rainfall_mm':       np.random.uniform(0, 200, n),
    'soil_moisture_pct': np.random.uniform(10, 100, n),
    'water_level_cm':    np.random.uniform(0, 300, n),
    'temp_celsius':      np.random.uniform(15, 40, n),
    'humidity_pct':      np.random.uniform(30, 100, n),
    'prev_24h_rain_mm':  np.random.uniform(0, 150, n),
}

df = pd.DataFrame(data)
df['flood_risk'] = (
    (df['rainfall_mm'] > 80) |
    (df['soil_moisture_pct'] > 85) |
    (df['water_level_cm'] > 200) |
    ((df['rainfall_mm'] > 50) & (df['prev_24h_rain_mm'] > 60))
).astype(int)

print(f"Dataset: {len(df)} samples | Flood cases: {df['flood_risk'].sum()}")

features = ['rainfall_mm','soil_moisture_pct','water_level_cm','temp_celsius','humidity_pct','prev_24h_rain_mm']
X, y = df[features], df['flood_risk']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

acc = accuracy_score(y_test, model.predict(X_test))
print(f"Model Accuracy: {acc*100:.2f}%")
print(classification_report(y_test, model.predict(X_test)))

path = os.path.join(os.path.dirname(__file__), 'flood_model.pkl')
with open(path, 'wb') as f:
    pickle.dump(model, f)
print(f"Saved: {path}")

sample = pd.DataFrame([{'rainfall_mm':120,'soil_moisture_pct':90,'water_level_cm':250,'temp_celsius':28,'humidity_pct':95,'prev_24h_rain_mm':80}])
print(f"Test Prediction: {model.predict_proba(sample)[0][1]*100:.1f}% flood probability")