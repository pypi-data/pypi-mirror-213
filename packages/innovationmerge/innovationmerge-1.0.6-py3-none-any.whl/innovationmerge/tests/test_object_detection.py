import os
from innovationmerge import cpuObjectDetectionTfLite, edgeObjectDetectionTfLite
from innovationmerge.src.utils.responses import load_labels, read_image

# Declare paths
cwd = os.getcwd()
model_path = os.path.join(cwd, "models", "ssd_mobilenet_v3_large_coco_2020_01_14")
model_file_path = os.path.join(model_path, "model.tflite")
labels_path = os.path.join(model_path, "labels.txt")
input_image_path = os.path.join(cwd, "data", "testdata", "images.jpg")


def test_cpu_object_detect():
    labels = load_labels(labels_path)
    cv2_image = read_image(input_image_path)
    detect_objects = cpuObjectDetectionTfLite(model_file_path)
    detection_result = detect_objects.detect(cv2_image, labels)
    print(detection_result)
    assert detection_result.get('detection')[0].get('label_class_name') == "cat"


def test_edge_object_detect():
    labels = load_labels(labels_path)
    cv2_image = read_image(input_image_path)
    detect_objects = edgeObjectDetectionTfLite(model_file_path)
    detection_result = detect_objects.detect(cv2_image, labels)
    print(detection_result)
    assert detection_result.get('detection')[0].get('label_class_name') == "cat"