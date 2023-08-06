import requests
import imghdr
from PIL import Image
from io import BytesIO
from collections import Counter


class ColorFinder:
    def __init__(self, image_url, num_colors):
        self.image_url = image_url
        self.num_colors = num_colors

    def get_common_colors(self):
        try:
            # Fetch the image from the URL
            response = requests.get(self.image_url)
            response.raise_for_status()

            # Check if the response contains valid image data
            image_format = imghdr.what(None, h=response.content)
            if image_format not in ['jpeg', 'png']:
                raise ValueError("Unsupported image format")

            # Open the image using Pillow
            image = Image.open(BytesIO(response.content))

            # Resize the image for faster processing
            image.thumbnail((200, 200))

            # Convert the image to RGB mode if it's not already
            image = image.convert('RGB')

            # Get the pixel data from the image
            pixels = list(image.getdata())

            # Count the occurrences of each color
            color_counts = Counter(pixels)

            # Get the most common colors
            most_common_colors = color_counts.most_common(self.num_colors)

            return most_common_colors

        except (requests.exceptions.RequestException, ValueError) as e:
            print("An error occurred:", str(e))
            return None
