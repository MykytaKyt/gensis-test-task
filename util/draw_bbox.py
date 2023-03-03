import cv2
from PIL import Image
import numpy as np


def draw_boxes_on_image(image, detections_df):
    """
    This function takes a PIL Image object and a Pandas DataFrame containing object detection results,
    and draws bounding boxes on the image based on the detection results.

    Parameters:
    image: PIL Image object. The input image.
    detections_df: Pandas DataFrame. The object detection results in a DataFrame format,
    containing columns for xmin, ymin, xmax, and ymax coordinates of the detected objects.

    Returns:
    pil_image: PIL Image object. The input image with bounding boxes drawn on it.
    """
    img = np.array(image)
    for _, row in detections_df.iterrows():
        x1, y1, x2, y2 = row[['xmin', 'ymin', 'xmax', 'ymax']].astype(int)
        img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    pil_image = Image.fromarray(img)
    return pil_image
