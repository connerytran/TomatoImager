

import cv2
import os
from datetime import datetime
photo_dir = '/home/tomato-imager/TomatoImager/Pis/pics/'
stop_path = '/tmp/stop.signal'

num_cams = 2

width = 4032
height = 3040
exposure = 1
gain = 100
brightness = 0
contrast = 20


def intialize_cam(cam_idx):
    """
    Initializes the camera given the index, creates and returns a cap object

    Params:
    cam_idx (int): idx for accessing each of the cameras
    """

    cap = cv2.VideoCapture(cam_idx)
    if not cap.isOpened():
        print('Cannot open camera')
        return None

    set_cam_ctrls(cap, width, height, exposure, gain, brightness, contrast)

    return cap



def take_picture(cap):
    """
    Given the camera, it will take a picture and save it to a folder

    Params:
    cap (cv2 VideoCapture): capture object for taking pictures
    """
    
    ret, frame = cap.read()
    if not ret:
        print("Cannot recieve frame.")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # imwrite_params = [cv2.IMWRITE_JPEG_QUALITY, 100]
        cv2.imwrite(f'{photo_dir}image_{timestamp}.jpg', frame)




def set_cam_ctrls(cap, width, height, exposure, gain, brightness, contrast):
    """
    Given the params and capture obj, will set the desired controls for the cap

    Params:
    cap (cv2 VideoCapture):
    width
    height
    exposure
    gain
    brihgtness
    contrast
    """

    # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure)

    cap.set(cv2.CAP_PROP_GAIN, gain)

    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    cap.set(cv2.CAP_PROP_CONTRAST, contrast)





def main():

    try:
        caps_array = []
        # Initializes all cams
        for cam_idx in range(0, num_cams * 2, 2):
            cap = intialize_cam(cam_idx)
            if cap is not None:
                caps_array.append(cap)
            else:
                print(f'Unable to initialize cam {cam_idx}')

        
        while True:
            
            for cap in caps_array:
                take_picture(cap)
            
            if os.path.exists(stop_path):
              os.remove(stop_path)
              break
    
    except KeyboardInterrupt:
        for cap in caps_array:
            cap.release()

    finally:
        for cap in caps_array:
            cap.release()




if __name__ == '__main__':
    main()


