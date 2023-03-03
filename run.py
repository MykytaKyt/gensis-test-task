import argparse
from api.app import run_server_api
from gradio_app import run_server
from settings import DEFAULT_PORT

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run YOLOv5 API or Gradio Demo')
    parser.add_argument('--api', action='store_true', default=False, help='Run the YOLOv5 Object Detection API')
    parser.add_argument('--demo', action='store_true', default=False, help='Run the YOLOv5 Object Detection Gradio Demo')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help='Port number to run the API or demo on')
    args = parser.parse_args()

    if args.api:
        run_server_api(port=args.port)
    elif args.demo:
        run_server(port=args.port)
    else:
        print(parser.print_help())
