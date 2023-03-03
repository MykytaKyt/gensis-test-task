# Genesis Test Task: Object Detection and Rendering API
This is a test task for the Genesis.
The project consists few parts: a YOLOv5-based object detection and rendering API, load test and gradio demo.

## Installation

Clone project ```$ git clone git@github.com:MykytaKyt/gensis-test-task.git```

### Install the requirements
Run  ```$ pip install -r requirements.txt```

### Configure the settings
The ```settings.py``` file contains configuration variables that you may need to adjust.

## Usage
### Starting the API server
To start the API server of Demo server, run the following command:
* ```$ python run.py --api --port <your_port>``` for API. 
This will start two API servers: one for object detection and one for rendering.

* ```$ python run.py --demo --port <your_port>``` for Gradio demo.
This will start server with demo.


### Making API requests
You can make API requests to the object detection API by sending a POST request with an image file to the /detect endpoint. Similarly, you can make requests to the rendering API by sending a POST request with an image file to the /render endpoint.

Here's an example using the request with /detect:

```
import requests

url = "http://0.0.0.0:5000/detect"

with open("/path/to/your/image", "rb") as f:
    image_bytes = f.read()
payload = image_bytes

headers = {
  'Content-Type': 'image/jpeg'
}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)

```
And here's an example using the request with /render:
```
import requests
import base64
from io import BytesIO
from PIL import Image

url = "http://0.0.0.0:5000/render"

with open("/path/to/your/image", "rb") as f:
    image_bytes = f.read()
payload = image_bytes

headers = {
  'Content-Type': 'image/jpeg'
}
response = requests.request("POST", url, headers=headers, data=payload)
imgdata = base64.b64decode(response.text)
filename = 'test.jpg'
with open(filename, 'wb') as f:
    f.write(imgdata)
```

## Testing the API

### Unit tests
First of all make sure that API server is running, if not use ```run.py```. And then you can run the automated tests by executing the following command:
```pytest api/tests/test_api.py```

### Load tests

To run locust load test, firstly you need start server using ```run.py```.
And the use ```locust -f api/tests/load_test.py```. 
After that in browser you need to specify number of users and serves address and port.

## Conclusion
This project provides a basic implementation of an object detection and rendering API using YOLOV5 and Flask.
Also project provides demo using Gradio and load test using Locust.
