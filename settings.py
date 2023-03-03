import os

basedir = os.path.abspath(os.path.dirname(__file__))

#Path to test image
TEST_IMAGE_PATH = os.path.join(basedir, 'api/tests/data/test.jpeg')

#Link to yolov5s model
MODEL_LINK = 'https://github.com/ultralytics/yolov5/releases/download/v5.0/yolov5s.pt'
#Model name
MODEL_NAME = 'yolov5s.pt'

# Detect endpoint
DETECT_ENDPOINT = '/detect'
# Render endpoint
RENDER_ENDPOINT = '/render'
# Default host address
DEFAULT_HOST = '0.0.0.0'
# Default host port
DEFAULT_PORT = 5000

#Filter for prediction confidence
DETECT_THRESHOLD = 0.25
