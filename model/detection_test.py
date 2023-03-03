import cv2
import torch
from model.initialize_model import yolo


def detect_from_local(image_path):
    """
    Detects objects in an image from a local file and displays the image with bounding boxes.

    Parameters
    ----------
    image_path : str
        The path to the image file.
    """
    detections = yolo.detect(image_path)
    img = cv2.imread(image_path)
    for _, row in detections.iterrows():
        x1, y1, x2, y2 = row[['xmin', 'ymin', 'xmax', 'ymax']].astype(int)
        img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":

    from settings import TEST_IMAGE_PATH
    detect_from_local(TEST_IMAGE_PATH)
