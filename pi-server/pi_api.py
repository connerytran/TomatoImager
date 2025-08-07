# import os
from flask import Flask, jsonify
import subprocess
from dotenv import load_dotenv

# load_dotenv()

# src_dir_path = os.getenv('src_dir_path')

src_dir_path = "/home/tomato-imager/TomatoImager/src/"
venv_python = "/home/tomato-imager/TomatoImager/venv/bin/python"

app = Flask(__name__)






# Retrieves the status of the pi
@app.route('/status', methods=['GET'])
def get_status():
  status = {"message": "Pi is online and ready",
            "device": "Pi3: Steve"}
  return jsonify(status)






# Begins taking pics
@app.route('/take_pictures', methods=['POST'])
def take_pictures():

  command = [venv_python, 'usb_cam.py'] #first arg ensures our venv is the py environment used

  try:
    subprocess.Popen(command, cwd=src_dir_path, stdout=subprocess.DEVNULL, text=True)
    message = {"message": "Taking pictures now."}
    return jsonify(message)
  except subprocess.CalledProcessError as e:
    message = {
      "message": "ERROR: The script failed to execute.",
      "status": "error",
      "details": e.stderr
    }
    return jsonify(message), 500
  except FileNotFoundError:
    message = {
      "message": "ERROR: File not found.",
      "status": "error",
    }    
    return jsonify(message), 500
  except Exception as e:
    message = {
      "message": "ERROR: Unexpected error.",
      "status": "error",
    }    
    return jsonify(message), 500




# Stops taking pics
@app.route('/stop_pictures', methods=['POST'])
def stop_pictures():

  command = [venv_python, 'stop_sig.py'] #first arg ensures our venv is the py environment used

  try:
    subprocess.run(command, cwd=src_dir_path, text=True, check=True)
    message = {"message": "Cameras stopped."}
    return jsonify(message)
  except subprocess.CalledProcessError as e:
    message = {
      "message": "ERROR: The script failed to execute.",
      "status": "error",
      "details": e.stderr
    }
    return jsonify(message), 500
  except FileNotFoundError:
    message = {
      "message": "ERROR: File not found.",
      "status": "error",
    }    
    return jsonify(message), 500
  except Exception as e:
    message = {
      "message": "ERROR: Unexpected error.",
      "status": "error",
    }    
    return jsonify(message), 500





if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)