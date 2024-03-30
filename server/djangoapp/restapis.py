# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv
from django.http import JsonResponse

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")


def get_request(endpoint, **kwargs):
    """
    Perform a GET request to the backend.
    """
    params = "&".join([f"{key}={value}" for key, value in kwargs.items()])
    request_url = f"{backend_url}{endpoint}?{params}"
    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")


def analyze_review_sentiments(text):
    """
    Analyze sentiments of a review using the sentiment analyzer.
    """
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Network exception occurred")


def get_dealerships(request, state="All"):
    """
    Retrieve a list of dealerships.
    """
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def post_review(data_dict):
    """
    Post a review to the backend.
    """
    request_url = f"{backend_url}/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
