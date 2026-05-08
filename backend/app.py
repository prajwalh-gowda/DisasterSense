from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle, pandas as pd, os
from datetime import datetime

try:
    from twilio.rest import Client
    TWILIO_OK = True
except:
    TWILIO_OK = False

app = Flask(__name__)
CORS(app)

TWILIO_SID     = "your_twilio_sid"
TWILIO_TOKEN   = "your_twilio_token"
TWILIO_FROM    = "+1234567890"
ALERT_TO       = "+91XXXXXXXXXX"

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'flood_model.pkl')

# LOAD MODEL
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded")
except Exception as e:
    print(f"Model load failed: {e}")
    model = None

flood_readings = []
quake_readings = []
alerts_log = []

# FLOOD PREDICTION
def predict_flood(d):
    features = ['rainfall_mm','soil_moisture_pct','water_level_cm','temp_celsius','humidity_pct','prev_24h_rain_mm']
    try:
        if model:
            df = pd.DataFrame([{k: d.get(k,0) for k in features}])
            prob = round(float(model.predict_proba(df)[0][1]) * 100, 1)
        else:
            prob = rule_based(d)
    except:
        prob = rule_based(d)

    risk = 'CRITICAL' if prob>=70 else 'WARNING' if prob>=40 else 'SAFE'
    return prob, risk

def rule_based(d):
    p = 0
    if d.get('rainfall_mm',0) > 80: p += 35
    if d.get('soil_moisture_pct',0) > 85: p += 25
    if d.get('water_level_cm',0) > 200: p += 30
    if d.get('prev_24h_rain_mm',0) > 60: p += 10
    return min(p,100)

# EARTHQUAKE
def predict_quake(d):
    mag = d.get('magnitude',0)
    risk = 'CRITICAL' if mag>=4 else 'WARNING' if mag>=3 else 'SAFE'
    intensity = 'STRONG' if mag>=4 else 'MODERATE' if mag>=3 else 'MINOR'
    return intensity, risk

# ALERT
def send_alert(location, details):
    if not TWILIO_OK:
        return False
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        client.messages.create(
            body=f"ALERT: {location} - {details}",
            from_=TWILIO_FROM,
            to=ALERT_TO
        )
        return True
    except:
        return False

@app.route('/health')
def health():
    return jsonify({"status":"ok"})

# FLOOD API
@app.route('/sensor-data', methods=['POST'])
def sensor_data():
    d = request.get_json()

    prob, risk = predict_flood(d)

    d.update({
        "node_id": d.get("node_id"),
        "flood_probability": prob,
        "risk_level": risk,
        "timestamp": datetime.now().isoformat()
    })

    flood_readings.append(d)

    return jsonify({
        "flood_probability": prob,
        "risk_level": risk
    })

# EARTHQUAKE API
@app.route('/quake-data', methods=['POST'])
def quake_data():
    d = request.get_json()

    intensity, risk = predict_quake(d)

    d.update({
        "node_id": d.get("node_id"),
        "intensity": intensity,
        "risk_level": risk,
        "timestamp": datetime.now().isoformat()
    })

    quake_readings.append(d)

    return jsonify({
        "intensity": intensity,
        "risk_level": risk
    })

# APIs
@app.route('/api/nodes/latest')
def latest_flood():
    seen = {}
    for r in reversed(flood_readings):
        if r['node_id'] not in seen:
            seen[r['node_id']] = r
    return jsonify(list(seen.values()))

@app.route('/api/quake/latest')
def latest_quake():
    seen = {}
    for r in reversed(quake_readings):
        if r['node_id'] not in seen:
            seen[r['node_id']] = r
    return jsonify(list(seen.values()))

@app.route('/api/nodes/<nid>/history')
def history(nid):
    return jsonify([r for r in flood_readings if r['node_id']==nid][-20:])

@app.route('/api/alerts')
def alerts():
    return jsonify(alerts_log)

@app.route('/api/stats')
def stats():
    return jsonify({
        "total": len(flood_readings)+len(quake_readings)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)