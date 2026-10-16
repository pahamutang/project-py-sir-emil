
import joblib
from pathlib import Path
from sklearn.tree import DecisionTreeClassifier

# Location where the trained model will be saved
MODEL_PATH = Path("student_pass_model.joblib")

# Sample training data: study hours
X = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]

# Sample labels: 0 = Fail, 1 = Pass
y = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]

# Train the model
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# Save the trained model
joblib.dump(model, MODEL_PATH)
print(f"Model saved to: {MODEL_PATH}")

# Load the saved model
loaded_model = joblib.load(MODEL_PATH)
print("Model loaded successfully!")

# Make three predictions using different study hours
study_hours_list = [[2], [5], [8]]

for hours in study_hours_list:
    prediction = loaded_model.predict([hours])[0]
    result = "Pass" if prediction == 1 else "Fail"

    print(f"Study hours: {hours[0]} -> Prediction: {result}")
