
import paramiko
import subprocess
import time
from os import system
from scp import SCPClient
adapter_name = 'wireless lan adapter wi-fi:'
default_dest_folder = 'LAB-C113-RESSOURCES'
check_mark = '===>'
# check_mark = check_mark.encode()

class Session:

    def __init__(self, host, ip, password):
        self.host = host
        self.ip = ip
        self.password = password
        self.client = None

    def make_ssh_connection(self):
        self.set_fingerprint()

        print(f"-------------------------------------------------------------------\nEtablishing SSH connection with {self.ip} .....")
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self.client.connect(self.ip, username=self.host, password=self.password)
            stdin, stdout, stderr = self.client.exec_command('cd')  # Example command
            print("\nOK: Connected to : " + stdout.read().decode())
            print(check_mark, end=' ')
            print(f'Etablish SSH Connection successfully with {self.ip}!!!')
        except Exception as e:
            print(f"Error ({self.host}@{self.ip}): {e}")




    def set_fingerprint(self):
        # Construct the SSH command with StrictHostKeyChecking=accept-new to accept the fingerprint and exit
        command = [
            "ssh",
            "-o", "StrictHostKeyChecking=accept-new",  # Automatically accept new host keys and store them
            "-o", "UserKnownHostsFile=~/.ssh/known_hosts",  # Ensure it stores the fingerprint in the known_hosts file
            f"{self.host}@{self.ip}"  # SSH user@host format
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
            # p.kill()
            print(check_mark, end=' ')
            p.kill()
            print("Set fingerprint successfully\n")

        except Exception as e:
            print(f"Error setting fingerprint: {e}\n")


    def copy_file_to_remote_client(self, file: str, r=False):

        try:
            # Now, use SCP to copy the file
            with SCPClient(self.client.get_transport()) as scp:
                print(f"Copying {file} to remote server...")
                scp.put(file, f'./{default_dest_folder}/', r)  # Upload file to the remote directory
                print(f"File '{file}' copied successfully to {self.ip}:./{default_dest_folder}/")
            if file is not None:
                print(f"Copying {file} to remote server...")
                print(check_mark, end=' ')
                print(f"File '{file}' copied successfully to {self.ip}:./{default_dest_folder}/\n")
                return self.ip
        except Exception as e:
            print(f"Error : {e}")


    def createFileDirectory(self, fileName:str, dir:bool):

        try:
            stdin, stdout, stderr = self.client.exec_command('dir /b')  # Example command
            result = stdout.read().decode().split()
            if fileName in result:
                print(check_mark, end=' ')
                print(f"File/Directory {fileName} already created")
            else :
                if dir:
                    print(f"\nCreating file/folder {fileName} .....")
                    self.client.exec_command(f'mkdir {fileName}')
                    print(check_mark, end=' ')
                    print(f"File/Directory {fileName} successfully created")
                else:
                    print('Not configured yet')

        except Exception as e:
            print(f"Error ({self.host}@{self.ip}): {e}")


    def close(self):
        # self.client.close()
        self.client = f"Client closed for {self.ip}!\n-----------------------------------------------------------------\n\n"
        print(check_mark, end=' ')
        print(self.client)

def ssh_connection(host: str, ip: str, password: str):
    print(f"\nEtablishing SSH connection with {ip} .....")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        set_fingerprint(host, ip)
        client.connect(ip, username=host, password=password)
        stdin, stdout, stderr = client.exec_command('cd')  # Example command
        print("OK: Connected to : " + stdout.read().decode())
    except Exception as e:
        print(f"Error ({host}@{ip}): {e}")
    finally:
        client.close()

def ssh_copy_file_to_remote_client(host: str, ip: str, password: str, file: str, r=False):
    # First, ensure the fingerprint is set
    # set_fingerprint(host, ip)
    try:
        # Establish SSH connection using paramiko
        print(f"\nEstablishing SSH connection to {host}@{ip}.....")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=host, password=password)
        print(f"OK: Connected to {host}@{ip}")

        # Now, use SCP to copy the file
        with SCPClient(client.get_transport()) as scp:
            print(f"Copying {file} to remote server...")
            scp.put(file, f'./{default_dest_folder}/', r)  # Upload file to the remote directory
            print(f"File '{file}' copied successfully to {ip}:./{default_dest_folder}/")
            client.close()
            print("SSH connection closed.\n")
            return ip

    except Exception as e:
        print(f"Error : {e}")

    finally:
        client.close()
        print("SSH connection closed.\n")




def get_my_ip():
    ip = []
    try:
        cmd = 'ipconfig'
        result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, ).stdout.lower()
        tab = [result for result in result.split('\n')]
        index_list = []
        for t in tab:
            if adapter_name in t:
                ip.append(t)
                index_list.append(tab.index(t))
        for row in tab[index_list[0]: index_list[0] + 7]:
            if 'ipv4' in row:
                ip.append(row.split(':')[1].strip())
                return ip

    except Exception as e:
        print(f"Error getting IP : {e}")


UNKNOWN = 'UNKNOWN'
def get_ip_list(network):

    split_add = network.split('.')
    split_add[-1] = '0'
    net_add = '.'.join(split_add)
    list = []
    print(f'My Ip : {network}\nNetwork address : {net_add}\n')
    try:
        cmd = f'nmap -sn {net_add}/24'
        result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, ).stdout.lower()
        tab = [result for result in result.split('\n')]
        index_list = []
        name, ip, mac = '', '', ''
        for t in tab[4:]:
            if 'nmap scan report' in t:
                info = t.split('for')[1]
                if len(info.split()) > 1:
                    name, ip = info.split()[0], info.split()[1].replace('(', '')
                else:
                    name, ip = UNKNOWN, info.split()[0]
            if 'mac address' in t:
                info = t.split(': ')[1]
                mac = info.split()[0]
                if ')' in ip:
                    list.append([name, ip.replace(')', ''), mac])
                else:
                    list.append([name, ip, mac])
            if network in t:
                info = t.split('for')[1]
                if len(info.split()) > 1 :
                    name, ip = info.split()[0], info.split()[1].replace('(', '')
                    list.append([name, ip.replace(')', ''), 'server'])
                else:
                    name, ip = UNKNOWN, info.split()[0]
                    list.append([name, ip, ''])

        return list



    #         for row in tab[index_list[0]+3:]:
    #             if len(row) > 0 :
    #                 if row.split()[2] == 'dynamic':
    #                     dynamic_ips.append(row.split())
    #                 elif row.split()[2] == 'static':
    #                     static_ips.append(row.split())


    except Exception as e:
        print(f"Error getting IP : {e}")
import threading


def get_devices():
    try:
        myIp = get_my_ip()[1]
        # dynamic_ips = [ip[1] for ip in get_ip_list(myIp)]
        # print(f'Dynamics : {get_ip_list(myIp)}')

        # for device in get_ip_list(myIp):
        #     print(f'Devices : {device}')
        return get_ip_list(myIp)
    except Exception as e:
        print(f"Error getting devices : {e}")
        return list()





# ssh_connection(host_, ip_[0], password_)

# def get_ip_list(network):
#     dynamic_ips = []
#     static_ips = []
#     print(f'Network : {network}')
#     try:
#         cmd = 'arp -a '
#         result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, ).stdout.lower()
#         tab = [result for result in result.split('\n')]
#         index_list = []
#         for t in tab:
#             if network in t:
#                 index_list.append(tab.index(t))
#                 for row in tab[index_list[0]+3:]:
#                     if len(row) > 0 :
#                         if row.split()[2] == 'dynamic':
#                             dynamic_ips.append(row.split())
#                         elif row.split()[2] == 'static':
#                             static_ips.append(row.split())
#         return [dynamic_ips, static_ips]
#
#     except Exception as e:
#         print(f"Error getting IP : {e}")
