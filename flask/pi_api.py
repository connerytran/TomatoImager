import os
from flask import Flask, jsonify
import subprocess
from dotenv import load_dotenv

load_dotenv()

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

  message = {"Aint work gang"}
  try:
    subprocess.run(command, cwd=src_dir_path, capture_output=True, text=True, check=True)
    message = {"message": "SUCCESS, taking pictures now..."}
    
  except subprocess.CalledProcessError as e:
    print(f"Error executing Globus transfer: {e}")
    print("STDOUT:", e.stdout)
    print("STDERR:", e.stderr)
  except FileNotFoundError:
    print("Error: 'globus' command not found. Is Globus CLI installed and in PATH?")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")

  return jsonify(message)




# Stops taking pics
@app.route('/stop_pictures', methods=['POST'])
def stop_pictures():

  command = [venv_python, 'stop_sig.py'] #first arg ensures our venv is the py environment used

  message = {"Aint work gang"}
  try:
    subprocess.run(command, cwd=src_dir_path, capture_output=True, text=True, check=True)
    message = {"message": "SUCCESS, taking pictures now..."}
    
  except subprocess.CalledProcessError as e:
    print(f"Error executing Globus transfer: {e}")
    print("STDOUT:", e.stdout)
    print("STDERR:", e.stderr)
  except FileNotFoundError:
    print("Error: 'globus' command not found. Is Globus CLI installed and in PATH?")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")


  return jsonify(message)





if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)