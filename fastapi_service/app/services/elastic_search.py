import requests
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


# Initialize the Elasticsearch client
client = Elasticsearch(
    "https://6a08a4951dff4c61a75fd673075afa86.us-central1.gcp.cloud.es.io:443",
    api_key="SU9MZHg0d0JiNlRXeGpHZ2Z6Nk86RlY1MjVrVGNUZW0yNVR4OXVXY056UQ=="
)
# Categories to fetch bestsellers from
categories = [
    #magazine missing, educational, live exploration
    
    "bestsellers_toys_and_games",
    "bestsellers_entertainment_collectibles",
    "bestsellers_us_live_explorations"
]



# Rainforest API key
api_key = '962BFCBC3E9C47E982C8FBF6DC793414'

def fetch_bestsellers(category_id):
    params = {
        'api_key': api_key,
        'type': 'bestsellers',
        'amazon_domain': 'amazon.com',
        'category_id': category_id
    }
    response = requests.get('https://api.rainforestapi.com/request', params)
    data = response.json()

    # Check if 'bestsellers' key exists and is not None
    if 'bestsellers' in data and data['bestsellers']:
        print(f"API Response for {category_id[:10]}: {data.get('bestsellers')[:2]}")  # Print first 2 products for debugging
    else:
        print(f"No bestsellers data found for category: {category_id}")
        return None  # Return None if no bestsellers data found

    return data

# Function to index products to Elasticsearch using bulk API
def index_to_elasticsearch(products):
    actions = [
        {
            "_index": "search-product-vendor",
            "_id": product.get("asin"),
            "_source": product
        }
        for product in products if product.get("asin")
    ]

    if actions:
        success, _ = bulk(client, actions)
        print(f"Indexed {success} products")
    else:
        print("No products to index")

# Main function
def main():
    for category in categories:
        print(f"Fetching bestsellers for category: {category}")
        bestsellers_data = fetch_bestsellers(category)
        if 'bestsellers' in bestsellers_data and bestsellers_data['bestsellers']:
            index_to_elasticsearch(bestsellers_data['bestsellers'])
        else:
            print(f"No bestsellers data found for category: {category}")

# Run the main function
if __name__ == "__main__":
    main()