from flask import Flask, json, request
from util import get_dominant_color, get_border_color
import requests


app = Flask(__name__)


@app.route('/')
def index():
    if 'src' not in request.args:
        obj = {
            "error": 'Please provide src for image!'
        }
        return json.dumps(obj, default=str)
    img_src = request.args['src']
    print(img_src)
    try:
        response = requests. get(img_src)
        file = open("image.png", "wb")
        file. write(response. content)
        file. close()
        border_color = get_border_color('image.png')
        dominant_color = get_dominant_color('image.png')
        obj = {
            "border_color": '#' + border_color,
            'dominant_color': '#' + dominant_color
        }
        # print(img_src)
        return json.dumps(obj, default=str)
    except:
        obj = {
            "error": "Please provide a valid URL for image source"
        }
        return json.dumps(obj, default=str)


if __name__ == '__main__':
    app.run(debug=True)
