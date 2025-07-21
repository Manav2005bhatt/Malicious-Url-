from flask import Flask, render_template, request
import joblib
import os
import pandas as pd
from .extract_features import extract_features

# Get the directory of the current file (app.py)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up to the root of the project (where 'frontend' folder resides)
# app.py is in src/backend/finaly/
# So, up 3 levels from app.py's directory to get to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..', '..'))

# Define the path to your templates folder
# It's at the project root, inside 'frontend', then 'templates'
TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT, 'frontend', 'templates')

# --- DEBUG PRINT STATEMENTS ---
print(f"DEBUG: app.py location: {os.path.abspath(__file__)}")
print(f"DEBUG: Calculated PROJECT_ROOT: {PROJECT_ROOT}")
print(f"DEBUG: Calculated TEMPLATE_FOLDER: {TEMPLATE_FOLDER}")
# --- END DEBUG PRINT STATEMENTS ---

STATIC_FOLDER = os.path.join(PROJECT_ROOT, 'frontend', 'static')

app = Flask(__name__,
            template_folder=TEMPLATE_FOLDER,
            static_folder=STATIC_FOLDER,
            static_url_path='/static') # This makes sure /static URL works

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

@app.route('/check_url', methods=['POST'])
def check_url():
    if request.method == 'POST':
        url = request.form['url']
        
        input_features = extract_features(url)
        
        result_prediction = model.predict([input_features])[0]

        if result_prediction == 1:
            result = "Malicious"
        else:
            result = "Safe"
        
        return render_template('result.html', url=url, result=result)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
