import gradio as gr
from util.image_utils import decode_img
from settings import DEFAULT_HOST, DEFAULT_PORT
from model.initialize_model import yolo


def predict(input_image, confidence):
    """
    This function takes an input image and a confidence score,
    and returns an output image with detected objects.
    If the input image is not a valid image file, it returns an error message.
    """
    try:
        return decode_img(yolo.render(input_image, confidence))
    except TypeError:
        return "Error: Input image must be a valid image file"


def run_server(port=DEFAULT_PORT):
    """
    This function launches the Gradio interface on the specified port.
    """
    iface.launch(server_name=DEFAULT_HOST, server_port=port, share=True)


iface = gr.Interface(
    fn=predict,
    inputs=[gr.Image(type="pil"), gr.inputs.Slider(minimum=0.1,
                                                   maximum=1,
                                                   step=0.1,
                                                   default=0.25)],
    outputs="image",
    title="YOLOv5 Object Detection",
    description="Detect objects in an image using the YOLOv5 model",
    live=True,
    layout="vertical"
)

if __name__ == "__main__":
    run_server(port=5000)
