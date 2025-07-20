import pandas as pd
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load dataset
df = pd.read_csv("urldata.csv")  # Replace with your CSV filename

# Feature extraction function
def extract_features(url):
    features = {}
    features['URL_Length'] = len(url)
    features['Num_Dots'] = url.count('.')
    features['Num_Hyphens'] = url.count('-')
    features['Num_At'] = url.count('@')
    features['Num_QuestionMarks'] = url.count('?')
    features['Num_Equals'] = url.count('=')
    features['Num_Underscore'] = url.count('_')
    features['Num_Slash'] = url.count('/')
    features['Num_Percent'] = url.count('%')
    features['Num_Colon'] = url.count(':')
    features['Num_Dollar'] = url.count('$')
    features['Num_Space'] = url.count(' ')
    features['Has_IP'] = int(bool(re.search(r'\d{1,3}(\.\d{1,3}){3}', url)))
    features['Has_HTTPS'] = int('https' in url.lower())
    features['Suspicious_Keywords'] = int(any(word in url.lower() for word in [
        'login', 'verify', 'account', 'update', 'secure', 'webscr', 'signin', 'banking'
    ]))
    return list(features.values())

# Prepare X and y
X = df['url'].apply(extract_features).tolist()
y = df['label'].apply(lambda x: 1 if x != 'benign' else 0)  # 1: Malicious, 0: Benign

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "improved_url_model.pkl")

# Evaluate
print("\nModel Performance:")
print(classification_report(y_test, model.predict(X_test)))

# Take input from user
print("\n🔐 Check URL:")
user_url = input("Enter a URL to check: ")
input_features = extract_features(user_url)
result = model.predict([input_features])[0]
print("Result:", "🔴 Malicious" if result == 1 else "🟢 Benign")
