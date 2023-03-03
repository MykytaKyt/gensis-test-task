import os
import torch
import base64
from io import BytesIO
from util.draw_bbox import draw_boxes_on_image
from util.image_utils import preprocess_image
from settings import MODEL_LINK, MODEL_NAME, DETECT_THRESHOLD


class YOLOv5:
    """
    Attributes
    ----------
    device : str
        the device used to run the model (default 'cuda')
    model : torch.nn.Module
        the YOLOv5 model loaded from file
        Parameters
    ----------
    device : str, optional
        the device used to run the model (default 'cuda')
    model_path : str, optional
        the path to the model file (default is current directory)
    model_link : str, optional
        the URL to download the model file (default is from settings.py)
    model_name : str, optional
        the name of the model file (default is from settings.py)
    """
    def __init__(self, device='cuda', model_path=None, model_link=None, model_name=None):
        self.device = device
        if model_path is None:
            model_path = os.path.abspath(os.path.dirname(__file__))
        if model_name is None:
            model_name = MODEL_NAME
        model_file_path = os.path.join(model_path, model_name)

        if not os.path.exists(model_file_path):
            if model_link is None:
                model_link = MODEL_LINK
            torch.hub.download_url_to_file(model_link, model_file_path)

        self.model = torch.hub.load('ultralytics/yolov5', 'custom',
                                    path=os.path.join(model_path, model_name),
                                    force_reload=True)
        self.model.to(self.device).eval()

    def detect(self, image, confidence_threshold=DETECT_THRESHOLD):
        """
        Detects objects in an image using the YOLOv5 model.

        Parameters
        ----------
        image : PIL.Image
            the image to detect objects in
        confidence_threshold : float, optional
            the confidence threshold for object detection (default from settings.py)

        Returns
        -------
        result : pandas.DataFrame
        a DataFrame containing the detected objects with columns 'class', 'confidence', 'xmin', 'ymin', 'xmax', 'ymax'
        """

        img_resized, scale_x, scale_y = preprocess_image(image)

        results = self.model(img_resized)
        detections = results.pandas().xyxy[0]
        detections = detections[detections['confidence'] > confidence_threshold]

        detections[['xmin', 'xmax']] *= scale_x
        detections[['ymin', 'ymax']] *= scale_y

        return detections

    def render(self, image, confidence_threshold=DETECT_THRESHOLD):
        """
        Renders an image with bounding boxes around detected objects using the YOLOv5 model.

        Parameters
        ----------
        image : PIL.Image
            the image to detect objects in and draw bounding boxes on images
        confidence_threshold : float, optional
            the confidence threshold for object detection (default from settings.py)

        Returns
        -------
        encoded_image : str
        a base64-encoded string of the rendered image
        """
        detections = self.detect(image, confidence_threshold)
        bbox_im = draw_boxes_on_image(image, detections)

        io_buf = BytesIO()
        bbox_im.save(io_buf, format='JPEG')
        encoded_image = base64.b64encode(io_buf.getvalue()).decode("utf-8")
        return encoded_image
