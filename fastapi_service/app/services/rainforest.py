import requests
import json
import os 

# Rainforest API key
api_key = os.getenv('RAINFOREST_API_KEY')

# Function to fetch categories with bestseller lists
def fetch_best_selling_categories():
    params = {
        'api_key': api_key,
        'domain': 'amazon.com',
        'type': 'bestsellers'  # Fetch categories compatible with bestseller requests
    }
    response = requests.get('https://api.rainforestapi.com/categories', params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch categories: {response.status_code}")
        print("Response:", response.text)
        return None

# Fetch and print best-selling categories
best_selling_categories = fetch_best_selling_categories()
if best_selling_categories:
    print(json.dumps(best_selling_categories, indent=4))