import os
import logging
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify, render_template
import pytesseract
import cv2
import requests
from PIL import Image
from PIL import ImageFilter
from io import StringIO

from ocr import process_image

app = Flask(__name__)
_VERSION = 1  # API version


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/v{}/ocr'.format(_VERSION), methods=["POST"])
def ocr():

    try:
        url = request.json['image_url']
        print (url)
        if 'jpg' in url:
            print('inside jpg')
            image = Image.open(url)
            print('got output')
            #image = _get_image(url)
            image.filter(ImageFilter.SHARPEN)
            print(pytesseract.image_to_string(image))
            
        
            output = pytesseract.image_to_string(image)
            print('got output')
            payload = "{test:"+output+"}"
            print(payload)
            return payload
    
        else:
            print('inside else')
            return jsonify({"error": "only .jpg files, please"})
    except:
       return jsonify(
        {"error": "Did you mean to send: {'image_url': 'some_jpeg_url'}"}
       )


@app.errorhandler(500)
def internal_error(error):
    print (str(error))  # ghetto logging


@app.errorhandler(404)
def not_found_error(error):
    print (str(error))

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: \
            %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
