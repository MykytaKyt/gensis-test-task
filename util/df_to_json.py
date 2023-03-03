def format_detections(detections):
    """
    This function takes a Pandas DataFrame containing object detection results and formats it
    into a dictionary with a list of object detections.

    Parameters:
    detections: Pandas DataFrame. The object detection results in a DataFrame format, containing columns for class,
    confidence, xmin, ymin, xmax, and ymax coordinates of the detected objects.

    Returns:
    formatted_detections: dict. A dictionary with a list of object detections.
    Each object detection is a dictionary containing keys for class, confidence, xmin, ymin, xmax, and ymax.
    """
    formatted_detections = {"objects": []}
    for _, row in detections.iterrows():
        obj = {
            "class": row["class"],
            "confidence": row["confidence"],
            "xmin": int(row["xmin"]),
            "ymin": int(row["ymin"]),
            "xmax": int(row["xmax"]),
            "ymax": int(row["ymax"]),
        }
        formatted_detections["objects"].append(obj)
    return formatted_detections
