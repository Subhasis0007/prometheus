import requests
import json
import os

def fetch_and_save_api_data(api_url, output_file):
    try:
        # Validate the API URL
        if not api_url.startswith("http"):
            raise ValueError("Invalid API URL. It must start with 'http://' or 'https://'.")
        
        # Make the API call
        response = requests.get(api_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Extract the JSON data from the response
            data = response.json()
            
            # Validate the output file path
            if not os.path.isdir(os.path.dirname(output_file)):
                raise FileNotFoundError(f"Output directory does not exist: {os.path.dirname(output_file)}")
            
            # Save the JSON data to a local file
            with open(output_file, 'w') as file:
                json.dump(data, file, indent=4)
            
            print(f"Data successfully saved to {output_file}")
        else:
            print(f"Failed to retrieve data: Status code {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred while making the request: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
api_url = "https://api.example.com/data"
output_file = "output_data.json"
fetch_and_save_api_data(api_url, output_file)