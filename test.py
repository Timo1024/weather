import requests
import json

# Define the endpoint URL
url = 'https://dwd.api.proxy.bund.dev/v30/stationOverviewExtended'

# Define the parameters
params = {
    'stationIds': '10865,G005'
}

# Define the headers
headers = {
    'Accept': 'application/json'
}

# Make the GET request
response = requests.get(url, headers=headers, params=params)

# Get the response body as a Python object
data = response.json()

# Open a file for writing
with open('response.json', 'w') as f:
    # Write the data to the file in a nicely formatted way
    json.dump(data, f, indent=4)

print('The response has been saved to response.json')

# Print the status code and the response body
print('Status Code:', response.status_code)
# print('Response Body:', response.json())