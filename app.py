from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("models/flood_model.pkl")
scaler = joblib.load("models/scaler.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    features = [float(request.form[f"feature{i}"]) for i in range(1, 21)]
    features = np.array(features).reshape(1, -1)
    features = scaler.transform(features)

    prediction = model.predict(features)[0]
    probability = round(prediction, 2)
    percent = round(probability * 100)

    if prediction < 0.4:
        risk = "Low Risk"
        emoji = "🟢"
        advice = "Flood risk is low. Continue regular monitoring."
        risk_class = "low"
    elif prediction < 0.7:
        risk = "Medium Risk"
        emoji = "🟡"
        advice = "Stay alert. Monitor weather updates and local authorities."
        risk_class = "medium"
    else:
        risk = "High Risk"
        emoji = "🔴"
        advice = "High flood risk. Take safety precautions immediately."
        risk_class = "high"

    return render_template(
        "index.html",
        prediction=probability,
        percent=percent,
        risk=risk,
        emoji=emoji,
        advice=advice,
        risk_class=risk_class
    )


if __name__ == "__main__":
    app.run(debug=True)