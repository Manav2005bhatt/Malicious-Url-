import re

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

