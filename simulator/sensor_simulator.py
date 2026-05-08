import time, random, requests
from datetime import datetime

API = "http://127.0.0.1:5000"

FLOOD_NODES = [
    {"id":"FL_001","location":"Panambur Beach",   "lat":12.9441,"lng":74.8059,"zone":"Coastal"},
    {"id":"FL_002","location":"Ullal Coast",       "lat":12.8031,"lng":74.8642,"zone":"Coastal"},
    {"id":"FL_003","location":"Netravathi River",  "lat":12.8698,"lng":74.8421,"zone":"River"},
    {"id":"FL_004","location":"Mangalore City",    "lat":12.8698,"lng":74.8430,"zone":"Urban"},
    {"id":"FL_005","location":"Surathkal Port",    "lat":13.0146,"lng":74.7937,"zone":"Port"},
]

QUAKE_NODES = [
    {"id":"EQ_001","location":"Western Ghats Fault",  "lat":12.9716,"lng":75.1200},
    {"id":"EQ_002","location":"Mangalore Offshore",   "lat":12.8500,"lng":74.7000},
    {"id":"EQ_003","location":"Coastal Seismic Zone", "lat":13.0000,"lng":74.8000},
    {"id":"EQ_004","location":"Konkan Fault Line",    "lat":12.7500,"lng":74.9500},
]

FLOOD_SCENARIOS = {
    "normal":   dict(rain=(5,40),   soil=(30,65),  water=(20,100), temp=(26,32), hum=(70,80), prev=(10,50)),
    "warning":  dict(rain=(60,110), soil=(75,88),  water=(160,220),temp=(27,30), hum=(88,94), prev=(60,90)),
    "critical": dict(rain=(130,190),soil=(90,100), water=(240,300),temp=(27,29), hum=(94,100),prev=(90,160)),
}

def flood_reading(node, sc="normal"):
    s = FLOOD_SCENARIOS[sc]
    return {
        "node_id":           node["id"],
        "location":          node["location"],
        "lat":               node["lat"],
        "lng":               node["lng"],
        "zone":              node["zone"],
        "timestamp":         datetime.now().isoformat(),
        "rainfall_mm":       round(random.uniform(*s["rain"]), 1),
        "soil_moisture_pct": round(random.uniform(*s["soil"]), 1),
        "water_level_cm":    round(random.uniform(*s["water"]), 1),
        "temp_celsius":      round(random.uniform(*s["temp"]), 1),
        "humidity_pct":      round(random.uniform(*s["hum"]), 1),
        "prev_24h_rain_mm":  round(random.uniform(*s["prev"]), 1),
    }

def quake_reading(node):
    mag = round(random.uniform(1.5, 4.8), 1)
    return {
        "node_id":   node["id"],
        "location":  node["location"],
        "lat":       node["lat"],
        "lng":       node["lng"],
        "timestamp": datetime.now().isoformat(),
        "magnitude": mag,
        "depth_km":  round(random.uniform(5, 25), 1),
        "p_wave":    round(mag*0.65+random.uniform(-0.2,0.2), 1),
        "s_wave":    round(mag*1.55+random.uniform(-0.3,0.3), 1),
        "vibration": min(100, round(mag*16+random.uniform(-5,5))),
    }

def run():
    print("🌊 DisasterSense Simulator — Mangalore Coastal")
    print(f"→ Backend: {API}\n")
    weights = ["normal","normal","normal","warning","critical"]
    cycle = 0
    while True:
        cycle += 1
        print(f"── Cycle {cycle} ─────────────────────────")
        for node in FLOOD_NODES:
            sc = random.choice(weights)
            r  = flood_reading(node, sc)
            try:
                res = requests.post(f"{API}/sensor-data", json=r, timeout=3).json()
                print(f"🌊 {node['id']} | {node['location']:20} | {sc.upper():8} | {res.get('flood_probability','?')}% | {res.get('risk_level','?')}")
            except:
                print(f"🌊 {node['id']} | {node['location']:20} | Backend offline")
        for node in QUAKE_NODES:
            r = quake_reading(node)
            try:
                res = requests.post(f"{API}/quake-data", json=r, timeout=3).json()
                print(f"🌍 {node['id']} | {node['location']:20} | M{r['magnitude']} | {res.get('intensity','?'):8} | {res.get('risk_level','?')}")
            except:
                print(f"🌍 {node['id']} | {node['location']:20} | Backend offline")
        print()
        time.sleep(5)

if __name__=="__main__":
    run()