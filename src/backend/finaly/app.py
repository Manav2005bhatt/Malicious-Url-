from flask import Flask, render_template, request
import joblib
import os
import pandas as pd
from .extract_features import extract_features

app = Flask(__name__)

# Get the directory of the current file (app.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the trained model
MODEL_PATH = os.path.join(BASE_DIR, "rf_model.pkl") # Use rf_model.pkl if that's your file
model = joblib.load(MODEL_PATH)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        url = request.form['url']
        features = pd.Series(extract_features(url)).to_frame().T
        prediction = model.predict(features)[0]
        result_text = 'Benign' if prediction == 0 else 'Malicious'
        return render_template('result.html', url=url, result=result_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
