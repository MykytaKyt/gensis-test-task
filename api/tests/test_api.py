import requests
import pytest
import base64
import io
from PIL import Image

from settings import DETECT_ENDPOINT, RENDER_ENDPOINT, TEST_IMAGE_PATH, DEFAULT_HOST, DEFAULT_PORT


@pytest.fixture(scope="module")
def test_image():
    image_path = TEST_IMAGE_PATH
    with open(image_path, "rb") as f:
        image_data = f.read()
    return image_data


def test_detect_api(test_image):
    """
    Test the object detection API endpoint.

    This function sends an image to the object detection endpoint and asserts
    that the response contains a list of dictionaries representing each detected object.
    Each object should contain the keys "class", "confidence", "xmin", "ymin", "xmax", "ymax".

    Parameters
    ----------
    test_image : bytes
        A byte string representing an image in JPEG format.

    Raises
    ------
    AssertionError
        If the response status code is not 200 or the response JSON does not
        contain a "objects" key or the "objects" value is not a list of dictionaries
        with the expected keys.
    """
    response = requests.post(f'http://{DEFAULT_HOST}:{DEFAULT_PORT}'+DETECT_ENDPOINT, data=test_image)
    assert response.status_code == 200

    response_json = response.json()
    assert isinstance(response_json, dict)
    assert "objects" in response_json

    objects = response_json["objects"]
    assert isinstance(objects, list)

    if not objects:
        assert objects == []
    else:
        for detection in objects:
            assert isinstance(detection, dict)
            assert all(key in detection for key in ["class", "confidence", "xmin", "ymin", "xmax", "ymax"])


def test_render_api(test_image):
    """
    Test the image rendering API endpoint.

    This function sends an image to the image rendering endpoint and asserts
    that the response is a JPEG encoded image.

    Parameters
    ----------
    test_image : bytes
        A byte string representing an image in JPEG format.

    Raises
    ------
    AssertionError
        If the response status code is not 200 or the response data is not a valid
        base64 encoded JPEG image or the image format is not "JPEG".
    """
    response = requests.post(f'http://{DEFAULT_HOST}:{DEFAULT_PORT}'+RENDER_ENDPOINT, data=test_image)
    assert response.status_code == 200

    image_data = base64.b64decode(response.text)
    assert isinstance(image_data, bytes)

    image = Image.open(io.BytesIO(image_data))
    assert isinstance(image, Image.Image)
    assert image.format == "JPEG"


def test_detect_api_wrong_data():
    """
    Test the object detection API endpoint with wrong input data type.

    This function sends a string to the object detection endpoint and asserts
    that the response is an error message.

    Raises
    ------
    AssertionError
        If the response status code is not 200 or the response text is not
        the expected error message.
    """
    response = requests.post(f'http://{DEFAULT_HOST}:{DEFAULT_PORT}'+DETECT_ENDPOINT, data="test")
    assert response.status_code == 200
    assert response.text == "Wrong data type. Make sure, that you use image"


def test_render_api_wrong_data():
    """
    Test the image rendering API endpoint with wrong input data type.

    This function sends a string to the image rendering endpoint and asserts
    that the response is an error message.

    Raises
    ------
    AssertionError
        If the response status code is not 200 or the response text is not
        the expected error message.
    """
    response = requests.post(f'http://{DEFAULT_HOST}:{DEFAULT_PORT}'+RENDER_ENDPOINT, data="test")
    assert response.status_code == 200
    assert response.text == "Wrong data type. Make sure, that you use image"


def test_detect_api_empty_data():
    """
    Test the image detect API endpoint with wrong input data type.

    This function sends an empty request to the image detection endpoint and asserts
    that the response is an error message.

    Raises
    ------
    AssertionError
        If the response status code is not 200 or the response text is not
        the expected error message.
    """
    response = requests.post(f'http://{DEFAULT_HOST}:{DEFAULT_PORT}'+DETECT_ENDPOINT, data=None)
    assert response.status_code == 200
    assert response.text == 'Error: Request data is empty'


def test_render_api_empty_data():
    """
    Test the image rendering API endpoint with wrong input data type.

    This function sends an empty request to the image rendering endpoint and asserts
    that the response is an error message.

    Raises
    ------
    AssertionError
        If the response status code is not 200 or the response text is not
        the expected error message.
    """
    response = requests.post(f'http://{DEFAULT_HOST}:{DEFAULT_PORT}'+RENDER_ENDPOINT, data=None)
    assert response.status_code == 200
    assert response.text == 'Error: Request data is empty'
