import cv2
import time

def read_image(input_image_path):
    cv2_image = cv2.imread(input_image_path)
    return cv2_image


def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]


def save_detection_image(detections, cv2_image, output_image_path):
    for detection in detections.get("detection"):
       xmin = detection.get("label_bounding_box")[0].get("x")
       ymin = detection.get("label_bounding_box")[0].get("y")
       xmax = detection.get("label_bounding_box")[1].get("x")
       ymax = detection.get("label_bounding_box")[1].get("y")
       cv2.rectangle(cv2_image, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)
        # Draw label
       object_name = detection["label_class_name"]
       confidence = detection["confidence"]
       label = '%s: %d%%' % (object_name, int(confidence*100))
       labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
       label_ymin = max(ymin, labelSize[1] + 10)
       cv2.rectangle(cv2_image, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED)
       cv2.putText(cv2_image, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.imwrite(output_image_path, cv2_image)


def show_detection_image(cv2_image):
    cv2.imshow('Detection', cv2_image)
    # Press any key to continue to next image, or press 'q' to quit
    if cv2.waitKey(0) == ord('q'):
        time.sleep(10)
    # Clean up
    cv2.destroyAllWindows()

