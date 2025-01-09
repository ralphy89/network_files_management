from os import system
url = 'https://github.com/ralphy89/network_files_management.git'
cmd1 = 'git pull origin master'
cmd2 = 'py -m pip install -r requirements.txt'
print(f'\n----------------------\nEXECUTING : {cmd1}\n----------------------\n')
system(cmd1)
print(f'\n----------------------\nEXECUTING : {cmd2}\n----------------------\n')
system(cmd2)
