import io
import base64

from locust import HttpUser, task, between

from PIL import Image
from settings import DETECT_ENDPOINT, RENDER_ENDPOINT, TEST_IMAGE_PATH


class APITestUser(HttpUser):
    """
    A Locust user class for testing API endpoints.

    Attributes
    ----------
    wait_time : between
        A wait time between requests to simulate user behavior.

    Methods
    -------
    detect()
        Sends a POST request to the detect endpoint and asserts the response.

    render()
        Sends a POST request to the render endpoint and asserts the response.
    """
    wait_time = between(1, 3)

    with open(TEST_IMAGE_PATH, "rb") as f:
        image_data = f.read()

    @task
    def detect(self):
        """
        Sends a POST request to the detect endpoint and asserts the response.
        """
        response = self.client.post(DETECT_ENDPOINT, data=self.image_data)

        assert response.status_code == 200
        response_json = response.json()
        assert isinstance(response_json, list)

    @task
    def render(self):
        """
        Sends a POST request to the render endpoint and asserts the response.
        """
        response = self.client.post(RENDER_ENDPOINT, data=self.image_data)

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "text/plain; charset=utf-8"
        assert response.headers["Content-Encoding"] == "gzip"
        assert response.headers["Transfer-Encoding"] == "chunked"
        assert response.headers["Connection"] == "keep-alive"

        image_data = base64.b64decode(response.text)
        assert isinstance(image_data, bytes)

        image = Image.open(io.BytesIO(image_data))
        assert isinstance(image, Image.Image)
        assert image.format == "JPEG"
        assert image.mode == "RGB"
