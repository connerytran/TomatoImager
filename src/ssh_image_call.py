
import paramiko
import os
from dotenv import load_dotenv

load_dotenv()

pi_user = os.getenv('pi_user')
pi_password = os.getenv('pi_password')
script_path = os.getenv('image_script_path')
num_of_pis = os.getenv('num_of_pis')
pi_hosts = []


## Reads the num_of_pis from env as an integer
if num_of_pis:
  try:
    num_of_pis = int(num_of_pis)
    print(num_of_pis)
  except ValueError:
    print("Invalid num_of_pis in .env")

## Reads in each pi to the pi_hosts array
for i in range(num_of_pis):
  host = os.getenv(f'pi_host_{i}')
  if host:
    pi_hosts.append(host)


def run_remote_script(host, username, password, script):
  try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    print(f"Connected to {host}")

    # stdin, stdout, stderr = client.exec_command(f"sudo python3 {script}")
    background_command = f"nohup sudo python3 {script} > /dev/null 2>&1 &"
    stdin, stdout, stderr = client.exec_command(background_command)
    print(f"Script on {host} ran")


    # for line in stdout:
    #   output = line.strip()
    #   print(f"{output}")
    
    # error_output = stderr.read().decode('utf-8').strip()
    # if error_output:
    #   print(f"Errors: {error_output}")

    client.close()
    return True
  
  except paramiko.AuthenticationException:
    print(f"Authentication failed for {host}")
    return False
  except paramiko.SSHException as e:
    print(f"SSH connection fail to {host} : {e}")
    return False
  except Exception as e:
    print(f"An error occured with {host}: {e}")
    return False
  
if __name__ == "__main__":

  try:
    for host in pi_hosts:
      run_remote_script(host, pi_user, pi_password, script_path)
  except KeyboardInterrupt:
    print("Stopping now.")


  
