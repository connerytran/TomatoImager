# TomatoImager



## Installation

** Install on both caller device and capture device **

1. Clone the repo
   ```sh
   git clone https://github.com/connerytran/TomatoImager.git
   ```
2. Create a python environment
   ```sh
   cd TomatoImager
   python3 -m venv your_venv_name 
   ```
3. Install library requirements
   ```sh
   source your_venv_name/bin/activate # Activation varies depending on os
   pip install -r requirements.txt
   ```

## Configuration

**Ensure both caller device and capture device are on the same network**
- Be sure to create your own .env file from the example given.

### Caller configurations
- pi_user and pi_password are the information needed to ssh into the pi to call the scripts.
- script_path is how you can choose to call the async script or non async script.
- stop_path is where the file that signals for the pi to stop will be.
- pi_host_* is where you would put the ip addresses of your capture devices

### Capture configurations
- photo_dir is the dir where you want to store the photos
- use:
  ```sh
  v4l2-ctl --list-devices
  v4l2-ctl -d /dev/videoX --list-formats-ext
  v4l2-ctl -d /dev/videoX --list-ctrls
  ```
  to know what formats your camera is suited for, as well as what camera properties it     can handle. The X in videoX is a placeholder for whatever camera listed.
- the camera properties can be adjusted to your liking, but ensure they are suitable for your camera

## Usage







   
