
import asyncio
import time
import cv2
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

photo_dir = os.getenv('photo_dir')
stop_path = os.getenv('stop_path')
num_of_cams = int(os.getenv('num_of_cams'))
width = int(os.getenv('width'))
height = int(os.getenv('height'))
exposure = int(os.getenv('exposure'))
gain = int(os.getenv('gain'))
brightness = int(os.getenv('brightness'))
contrast = int(os.getenv('contrast'))


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



async def take_picture(cap, cam_idx):
    """
    Given the camera, it will take a picture and save it to a folder

    Params:
    cap (cv2 VideoCapture): capture object for taking pictures
    """
    try:
        # start = time.perf_counter()
        while True:
            print(f"Camera {cam_idx} taking pic")
            start_time = time.perf_counter()
            ret, frame = await asyncio.to_thread(cap.read) # use background thread to run the I/O
            if not ret:
                print("Cannot recieve frame.")
            else:
                end_time = time.perf_counter()
                duration = end_time - start_time
                print(f"Camera {cam_idx} pic taken in {duration} seconds")
                await asyncio.to_thread(save_picture, frame, cam_idx)
                

            if os.path.exists(stop_path):
                return
            
            # end = time.perf_counter()
            
            # if end - start > 10:
            #     return
    
    except KeyboardInterrupt:
        return
    finally:
        return


def save_picture(frame, cam_idx):
    """
    """
    print(f"Camera {cam_idx} saving pic")
    start_time = time.perf_counter()
    imwrite_params = [cv2.IMWRITE_JPEG_QUALITY, 100]
    end_time = time.perf_counter()
    duration = end_time - start_time    
    timestamp = datetime.now()
    cv2.imwrite(f'{photo_dir}image_{timestamp}_cam-{cam_idx}.jpg', frame, imwrite_params)

    print(f"Camera {cam_idx} pic saved in {duration} seconds")
    
    


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





async def main():
    
    try:
        caps_array = []
        # Initializes all cams and adds them to caps_array
        for cam_idx in range(0, num_of_cams * 2, 2):
            cap = intialize_cam(cam_idx)
            if cap is not None:
                caps_array.append(cap)
            else:
                print(f'Unable to initialize cam {cam_idx}')
        
        # create coroutine object array with take_picutre async function for each camera
        coroutine_objs = [take_picture(cap, cam_idx) for cam_idx, cap in enumerate(caps_array)]
        # turn them into tasks by awaiting them
        await asyncio.gather(*coroutine_objs)
    
    except KeyboardInterrupt:
        for cap in caps_array:
            cap.release()

    finally:
        for cap in caps_array:
            cap.release()
        if os.path.exists(stop_path):
            os.remove(stop_path)




if __name__ == '__main__':
    asyncio.run(main())


