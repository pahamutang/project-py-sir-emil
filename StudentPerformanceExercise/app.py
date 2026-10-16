
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the saved model from Exercise 1
model = joblib.load("student_pass_model.joblib")


@app.route("/")
def home():
    return jsonify({
        "message": "Student Performance Prediction API is running!"
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please send a valid JSON object."
        }), 400

    # Check required inputs
    if "study_hours" not in data or "attendance_percentage" not in data:
        return jsonify({
            "error": "Both study_hours and attendance_percentage are required."
        }), 400

    try:
        study_hours = float(data["study_hours"])
        attendance = float(data["attendance_percentage"])
    except (TypeError, ValueError):
        return jsonify({
            "error": "Study hours and attendance must be numbers."
        }), 400

    if study_hours < 0:
        return jsonify({
            "error": "Study hours cannot be negative."
        }), 400

    if not 0 <= attendance <= 100:
        return jsonify({
            "error": "Attendance percentage must be between 0 and 100."
        }), 400

    # The current model uses study hours only
    prediction = model.predict([[study_hours]])[0]
    result = "Pass" if prediction == 1 else "Fail"

    return jsonify({
        "study_hours": study_hours,
        "attendance_percentage": attendance,
        "prediction": result,
        "note": "Prediction is based on study hours only; attendance does not affect the current model."
    })


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
