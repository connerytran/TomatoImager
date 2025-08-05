import subprocess
from datetime import datetime
import os
from dotenv import load_dotenv
import sys

load_dotenv()


# Your Globus Endpoint IDs
PI_ENDPOINT_ID = os.getenv('PI_ENDPOINT_ID')
DEST_ENDPOINT_ID = os.getenv('DEST_ENDPOINT_ID')
num_of_cams = os.getenv('num_of_cams')

# Paths (ensure these are correct on your Pi and destination)
SOURCE_DIR = os.getenv('photo_dir') # Example path
DEST_DIR = os.getenv('dest_dir')


if len(sys.argv) < 2:
    print("Error: No filename provided. Usage: python3 script.py <filename>")
    sys.exit(1)

foldername = sys.argv[1]
print(foldername)
input("continue?")

def globus_transfer():
    transfer_label = f"HAWKEYE_UPLOAD_{datetime.now()}"

    # Ensure the source directory exists before trying to transfer
    if not os.path.exists(SOURCE_DIR):
        print(f"Error: Source directory '{SOURCE_DIR}' does not exist.")
        return

# globus transfer d4eb6d3e-4c86-11f0-a629-0affcfc1d1e5:/home/tomato-imager/TomatoImager/pics/ 2f7f6170-8d5c-11e9-8e6a-029d279f7e24:/rs1/shares/cals-research-station/clinton/tomato-imager/pi3-pics/ --recursive --label "HAWKEYE_upload"

    command = [
        "globus", "transfer", f"{PI_ENDPOINT_ID}:{SOURCE_DIR}",
        f"{DEST_ENDPOINT_ID}:{DEST_DIR}",
        "--recursive", "--label", transfer_label, "--notify", 'failed'
    ]

    separator = ' '
    print(f"Initiating Globus transfer with command: {separator.join(command)}")

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Globus Transfer Initiated Successfully!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr) # CLI often prints task ID to stderr on success

    except subprocess.CalledProcessError as e:
        print(f"Error executing Globus transfer: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
    except FileNotFoundError:
        print("Error: 'globus' command not found. Is Globus CLI installed and in PATH?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


globus_transfer()

# for cam_idx in range(num_of_cams):
#   globus_transfer()
