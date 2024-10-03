import socket 
import os

from argparse import ArgumentParser

def run_client(filename, ip):
  sip = ip
  sport = 5001
  s = socket.socket()
  s.connect((sip, sport))
  s.send(f"{filename}".encode())
  received = s.recv(1024).decode()
  if received == "EXISTS":
    print("File exists")
  elif received == "ERROR":
    print("File not found")
  else:
    print("Error")

if __name__ == "__main__":
  parser = ArgumentParser(description="File transfer client")
  parser.add_argument('--file', '-f',
                    type=str,
                    help="File to download",
                    default="file.txt")
  
  parser.add_argument('--ip', '-i',
                    type=str,
                    help="ip address of the server",
                    default="192.168.1.1")
  
  args = parser.parse_args()
  filename = args.file
  run_client(filename)