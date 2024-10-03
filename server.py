import socket 
import os

from argparse import ArgumentParser

def run_server(path):
  basepath = path
  s = socket.socket()
  s.bind(("", 5001))
  s.listen(1)
  while True:
    client_socket, address = s.accept() 
    received = client_socket.recv(1024).decode()
    if not received:    
      break
    if os.path.exists(os.path.join(basepath, received)):
      client_socket.send("EXISTS".encode())
    else:
      client_socket.send("ERROR".encode())
    client_socket.close()

if __name__ == "__main__":
  parser = ArgumentParser(description="File transfer client")
  parser.add_argument('--path', '-p',
                    type=str,
                    help="base path to search for files",
                    default="./")
  args = parser.parse_args()
  path = args.path
  run_server(path)  