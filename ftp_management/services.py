import paramiko
import subprocess
import time
from os import system
from scp import SCPClient
system('cls')


def set_fingerprint(host, ip):
    # Construct the SSH command with StrictHostKeyChecking=accept-new to accept the fingerprint and exit
    command = [
        "ssh",
        "-o", "StrictHostKeyChecking=accept-new",  # Automatically accept new host keys and store them
        "-o", "UserKnownHostsFile=~/.ssh/known_hosts",  # Ensure it stores the fingerprint in the known_hosts file
        f"{host}@{ip}"  # SSH user@host format

    ]

    try:
        # Run the command as a subprocess
        p = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Capture the output and errors
        # output, errors = p.communicate()
        p.kill()
        print("OK: Set fingerprint ....")

    except Exception as e:
        print(f"An error occurred: {e}")



def ssh_connection(host: str, ip: str, password: str):
    print("Etablishing SSH connection .....")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        set_fingerprint(host, ip)
        client.connect(ip, username=host, password=password)
        stdin, stdout, stderr = client.exec_command('cd')  # Example command
        print("OK: Connected to : " + stdout.read().decode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

def ssh_copy_file_to_remote_client(host: str, ip: str, password: str, file: str, r=False):
    # First, ensure the fingerprint is set
    set_fingerprint(host, ip)

    try:
        # Establish SSH connection using paramiko
        print("Establishing SSH connection .....")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=host, password=password)
        print(f"OK: Connected to {host}@{ip}")

        # Now, use SCP to copy the file
        with SCPClient(client.get_transport()) as scp:
            print(f"Copying {file} to remote server...")
            scp.put(file, './LAB-C113-RESSOURCES/', r)  # Upload file to the remote directory

        print(f"File '{file}' copied successfully to {ip}:./LAB-C113-RESSOURCES/")

    except Exception as e:
        print(f"Error : {e}")

    finally:
        client.close()
        print("SSH connection closed.")








# ssh_connection(host_, ip_[0], password_)
# ssh_copy_file_to_remote_client(host_, ip_[0], password_, 'test', True)

