import requests

# Replace with your local FastAPI URL
url = "http://127.0.0.1:8000/submit/farmer"

# Test data
data = {
    "batch_id": "BATCH123",
    "crop_name": "Tulsi",
    "weight": "100kg",
    "stakeholder": "farmer"
}

# Files to upload
files = {
    "image": open("C:\\Users\\mahik\\Downloads\\Canon_PowerShot_S40.jpg", "rb")  # Replace with a local test image path
}

# Send POST request
response = requests.post(url, data=data, files=files)

# Print response
print(response.status_code)
print(response.text)   # instead of response.json()
