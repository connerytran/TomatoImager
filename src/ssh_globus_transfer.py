
import paramiko
import os
from dotenv import load_dotenv

load_dotenv()

pi_user = os.getenv('pi_user')
pi_password = os.getenv('pi_password')
script_path = os.getenv('transfer_script_path')
venv_path = os.getenv('venv_path')
num_of_pis = os.getenv('num_of_pis')
pi_hosts = []
invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', ' ']



def run_remote_script(host, username, password, script, foldername):
  try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    print(f"Connected to {host}")

    stdin, stdout, stderr = client.exec_command(f"source {venv_path} && python3 {script} {foldername}")

    # background_command = f"source {venv_path} && python3 {script} {foldername} > /dev/null 2>&1 &"
    # stdin, stdout, stderr = client.exec_command(background_command)
    print(f"Script on {host} ran")

    for line in stdout:
      output = line.strip()
      print(f"{output}")
    
    error_output = stderr.read().decode('utf-8').strip()
    if error_output:
      print(f"Errors: {error_output}")

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

  ## Reads the num_of_pis from env as an integer
  if num_of_pis:
    try:
      num_of_pis = int(num_of_pis)
      # print(num_of_pis)
    except ValueError:
      print("Invalid num_of_pis in .env")

  ## Reads in each pi to the pi_hosts array
  for i in range(num_of_pis):
    host = os.getenv(f'pi_host_{i}')
    if host:
      pi_hosts.append(host)

  try:

    foldername = None
    # foldername = input("plz make an input testing\n")
    while True:
      foldername = input("Foldername CANNOT include: <, >, :, \", /, \\, |, ?, *, or spaces." \
      "\nEnter a valid foldername: ")
      
      if not foldername:
        print("Foldername cannot be empty.")
        continue

      if any(char in foldername for char in invalid_chars):
        print("Foldername has invalid chars, try again.")
        continue

      print(f"Foldername accepted: {foldername}\n")
      break
    print(foldername)
    for host in pi_hosts:
      run_remote_script(host, pi_user, pi_password, script_path, foldername)
  except KeyboardInterrupt:
    print("Stopping now.")


  
