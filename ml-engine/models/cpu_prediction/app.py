from flask import Flask, render_template, request
from flask_cors import CORS
import pickle
import numpy as np

import os

# Get the directory of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "pickle_files", "model_before.pkl")

# Load trained model
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", prediction=None)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Check if request is JSON or Form
        if request.is_json:
            data = request.get_json()
            energy = float(data.get("energy", 0))
            age = int(data.get("age", 0))
            duration = float(data.get("duration", 0))
            time_of_day = int(data.get("time_of_day", 0))
            day_of_week = int(data.get("day_of_week", 0))
            charger_type = int(data.get("charger_type", 0))
            user_type = int(data.get("user_type", 0))
        else:
            energy = float(request.form["energy"])
            age = int(request.form["age"])
            duration = float(request.form["duration"])
            time_of_day = int(request.form["time_of_day"])
            day_of_week = int(request.form["day_of_week"])
            charger_type = int(request.form["charger_type"])
            user_type = int(request.form["user_type"])

        # Compute charging rate automatically
        rate = energy / duration if duration > 0 else 0

        # Create input array
        sample = np.array([[energy, rate, age, duration,
                            time_of_day, day_of_week, charger_type, user_type]])

        # Predict cost per unit
        prediction = round(model.predict(sample)[0], 3)

        if request.is_json:
            return {"prediction": prediction}
        
        return render_template("index.html", prediction=prediction)

    except Exception as e:
        if request.is_json:
            return {"error": str(e)}, 400
        return render_template("index.html", prediction=f"Error in input: {e}")

if __name__ == "__main__":
    app.run(debug=True)