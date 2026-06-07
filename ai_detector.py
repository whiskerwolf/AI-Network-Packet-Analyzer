from sklearn.ensemble import IsolationForest

traffic_data = []

ai_model = IsolationForest(
    contamination=0.05,
    random_state=42
)


def detect_ai_anomaly(packet_size):
    global traffic_data

    traffic_data.append([packet_size])

    if len(traffic_data) < 50:
        return "Learning..."

    ai_model.fit(traffic_data)

    prediction = ai_model.predict(
        [[packet_size]]
    )

    if prediction[0] == -1:
        return "⚠ Suspicious"

    return "Normal"
