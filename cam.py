import cv2
import time

def find_camera_indices(max_index=15, timeout=2):
    valid_indices = []
    for index in range(max_index):
        start_time = time.time()
        cap = cv2.VideoCapture(index)
        while not cap.isOpened() and (time.time() - start_time) < timeout:
            time.sleep(0.1)
            cap = cv2.VideoCapture(index)
        
        if cap.isOpened():
            print(f"Camera found at index {index}")
            valid_indices.append(index)
            cap.release()
        else:
            print(f"No camera at index {index}")
    return valid_indices

if __name__ == "__main__":
    camera_indices = find_camera_indices()
    if camera_indices:
        print(f"Available camera indices: {camera_indices}")
    else:
        print("No cameras found.")
