import os
import socket
import sys
import time

from protocol import DATA, END, Message, recv_message, send_message

serverPort = 20003

# Downloaded files are saved here (NOT in the server's directory: in Mininet all
# hosts share the same file system, so we would overwrite the original files).
DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "downloads")

USAGE = f"""usage:
  python3 {sys.argv[0]} SERVER_IP             receive dummy data (what the skeleton does now)
  python3 {sys.argv[0]} SERVER_IP list        print the files available on the server
  python3 {sys.argv[0]} SERVER_IP get FILE    download FILE into downloads/"""


def receive_dummy_data(s):
  """What the client does now: receive DATA messages until END.

  Returns the number of bytes received.
  """
  received = 0
  while True:
    msg = recv_message(s)
    if msg is None:
      raise ConnectionError("the server closed the connection before END")
    if msg.t == END:
      return received
    if msg.t == DATA:
      received += len(msg.payload)


def list_files(s):
  """Ask the server for the list of available files and print it, one per line."""
  # TODO (Part 1)
  raise NotImplementedError("list is not implemented yet")


def get_file(s, name):
  """Download the file `name` from the server into DOWNLOAD_DIR.

  Returns the number of bytes received. If the server reports an error (e.g. the
  file does not exist), print it and return None.
  """
  # TODO (Part 1): send the request, then receive the file like receive_dummy_data()
  # does, writing each chunk to os.path.join(DOWNLOAD_DIR, name) as it arrives.
  os.makedirs(DOWNLOAD_DIR, exist_ok=True)
  raise NotImplementedError("get is not implemented yet")


def main():
  if len(sys.argv) < 2:
    sys.exit(USAGE)
  serverIP = sys.argv[1]
  command = sys.argv[2:]

  start = time.perf_counter()
  s = socket.create_connection((serverIP, serverPort))

  if not command:
    # Only works with the skeleton server. Once your server waits for a request,
    # this would block forever: remove it.
    name, size = "dummy", receive_dummy_data(s)
  elif command == ["list"]:
    list_files(s)
    name, size = None, None
  elif len(command) == 2 and command[0] == "get":
    name, size = command[1], get_file(s, command[1])
  else:
    sys.exit(USAGE)

  s.close()
  end = time.perf_counter()

  # Do not change this line: the notebook reads it to collect your measurements.
  # The time includes connection setup, the request and the whole transfer.
  if size is not None:
    print(f"RESULT {name} {size} {end - start:.6f}")


if __name__ == "__main__":
  main()
