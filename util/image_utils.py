import io
import base64
from PIL import Image


def preprocess_image(image, size=(640, 640)):
    """
    This function takes an image file path or a PIL Image object and preprocesses it by resizing
    it to a specified size, converting it to RGB mode, and calculating the scaling factors.
    It returns the resized image, along with the scaling factors.

    Parameters:
    image: str or PIL Image object. The path to the image file or a PIL Image object.
    size: tuple. The target size of the image. Default is (640, 640).

    Returns:
    img_resized: PIL Image object. The resized image in RGB mode.
    scale_x: float. The scaling factor along the x-axis.
    scale_y: float. The scaling factor along the y-axis.
    """
    if isinstance(image, str):
        with open(image, 'rb') as f:
            img_data = f.read()
        img = Image.open(io.BytesIO(img_data)).convert('RGB')
    elif isinstance(image, Image.Image):
        img = image.convert('RGB')
    else:
        raise TypeError("image must be a file path, or PIL image")

    w, h = img.size
    img_resized = img.resize(size, resample=Image.BILINEAR)

    scale_x = w / size[0]
    scale_y = h / size[1]

    return img_resized, scale_x, scale_y


def decode_img(msg):
    """
    This function takes a Base64-encoded string and decodes it into a PIL Image object.

    Parameters:
    msg: str. The Base64-encoded string.

    Returns:
    img: PIL Image object. The decoded image.
    """
    msg = base64.b64decode(msg)
    buf = io.BytesIO(msg)
    img = Image.open(buf)
    return img
