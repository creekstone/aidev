import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Replace YOUR_API_KEY with your actual API key
api_key = os.getenv('OPENAPI_KEY')

# Construct the path to the Downloads folder
downloads_folder = os.path.expanduser('~/Downloads')

def get_unique_filename(filename):
  # Get the list of all files in the Downloads folder
  filenames = os.listdir(downloads_folder)
  
  # If the given filename is not in the list, return it as is
  if filename not in filenames:
    return filename

  # If the given filename is already in the list, create a new filename by appending
  # the next sequential integer to it
  i = 1
  while True:
    new_filename = f"{filename} ({i})"
    if new_filename not in filenames:
      return new_filename
    i += 1


# Set the prompt that you want Dall-E to generate an image for
prompt = "the inside of a triangle filled with the full spectrum of light from red to orange to yellow to green to blue to violet"

# Set the endpoint URL for the Dall-E API
endpoint_url = "https://api.openai.com/v1/images/generations"

# Set the headers for the API request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Set the data for the API request
data = """
{
    """
data += f'"model": "image-alpha-001",'
data += f'"prompt": "{prompt}",'
data += """
    "num_images":1,
    "size":"1024x1024",
    "response_format":"url"
}
"""

# Send the request to the API and get the response
response = requests.post(endpoint_url, headers=headers, data=data)

# Check the status code of the response
if response.status_code == 200:
    # Get the image URL from the response
    image_url = response.json()['data'][0]['url']

    # Download the image
    image_data = requests.get(image_url).content

    # Save the image to the downloads folder
    with open(os.path.join(downloads_folder, get_unique_filename("image.jpg")), "wb") as f:
        f.write(image_data)
else:
    # Print an error message if the request fails
    print("Failed to generate image")
