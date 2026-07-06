from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("models/flood_model.pkl")
scaler = joblib.load("models/scaler.pkl")

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    features = [float(request.form[f"feature{i}"]) for i in range(1, 21)]
    features = np.array(features).reshape(1, -1)
    features = scaler.transform(features)

    prediction = model.predict(features)[0]

    if prediction < 0.4:
        risk = "Low Risk 🟢"
    elif prediction < 0.7:
        risk = "Medium Risk 🟡"
    else:
        risk = "High Risk 🔴"

    return render_template(
        "index.html",
        prediction=round(prediction, 2),
        risk=risk
    )
if __name__ == "__main__":
    app.run(debug=True)