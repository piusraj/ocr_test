import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from io import StringIO


def process_image(url):
    image = _get_image(url)
    image.filter(ImageFilter.SHARPEN)
    print(pytesseract.image_to_string(image))
    return pytesseract.image_to_string(image)


def _get_image(url):
    return Image.open(StringIO(requests.get(url).content))
