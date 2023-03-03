import io
import base64
from io import BytesIO
from flask import Flask, request, jsonify
from PIL import Image
from settings import DETECT_ENDPOINT, RENDER_ENDPOINT, DEFAULT_HOST, DEFAULT_PORT
from util.df_to_json import format_detections
from util.draw_bbox import draw_boxes_on_image
from model.initialize_model import yolo

app = Flask(__name__)


def detect(image):
    """
    Detects objects in an image.

    Parameters
    ----------
    image : PIL.Image.Image
        The image to detect objects in.

    Returns
    -------
    response : dict
        A dictionary containing the detected objects and their properties.
    """
    detections = yolo.detect(image)
    response = format_detections(detections)
    return response


def render(image):
    """
    Renders bounding boxes on an image.

    Parameters
    ----------
    image : PIL.Image.Image
        The image to render bounding boxes on.

    Returns
    -------
    encoded_image : str
        A base64-encoded string representation of the image with the
        bounding boxes rendered on it.
    """

    detections = yolo.detect(image)
    bbox_im = draw_boxes_on_image(image, detections)

    io_buf = BytesIO()
    bbox_im.save(io_buf, format='JPEG')
    encoded_image = base64.b64encode(io_buf.getvalue()).decode("utf-8")
    return encoded_image


@app.route('/')
def index():
    return 'Server Works!'


@app.route(DETECT_ENDPOINT, methods=['POST'])
def detect_api():
    """
    API endpoint for detecting objects in an image.

    Returns
    -------
    flask.Response
        A Flask response object containing the detected objects and their
        properties in JSON format.
    """
    if request.method != 'POST':
        return
    if not request.data:
        return "Error: Request data is empty"
    try:
        im_data = request.data
        im = Image.open(io.BytesIO(im_data))

        response = detect(im)
        return jsonify(response)
    except Exception:
        return f"Wrong data type. Make sure, that you use image"


@app.route(RENDER_ENDPOINT, methods=['POST'])
def render_api():
    """
    API endpoint for rendering bounding boxes on an image.

    Returns
    -------
    response : str
        A base64-encoded string representation of the image with the
        bounding boxes rendered on it.
    """
    if request.method != 'POST':
        return
    if not request.data:
        return "Error: Request data is empty"
    try:
        im_data = request.data
        im = Image.open(io.BytesIO(im_data))

        response = render(im)
        return response
    except Exception:
        return f"Wrong data type. Make sure, that you use image"


def run_server_api(port=DEFAULT_PORT):
    """
    Runs the API server.

    Parameters
    ----------
    port : int, optional
        The port to run the server on (default is 5000).
    """
    app.run(host=DEFAULT_HOST, port=port, debug=False)


if __name__ == "__main__":
    run_server_api(port=5000)
