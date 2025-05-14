

import paramiko

pi_hosts = [
  "10.152.44.200"
]

pi_user = "tomato-imager"
pi_password = "makerspace"
script_path = "/home/tomato-imager/TomatoImager/Pis/imageScript"
stop_path = '/tmp/stop.signal'


def stop_remote_script(host, username, password, script):
  try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    print(f"Connected to {host}")

    stdin, stdout, stderr = client.exec_command(f"touch {stop_path}")
    print(f"Stopping script")

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
      stop_remote_script(host, pi_user, pi_password, script_path)
    print("Script stopped.")
  except KeyboardInterrupt:
    print("Stopping now.")


  
