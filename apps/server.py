import os
import socket

from protocol import DATA, END, Message, recv_message, send_message

localIP = "0.0.0.0"  # all interfaces
localPort = 20003
chunkSize = 64 * 1024  # bytes of data per DATA message

# The directory the server shares. Only files in this directory can be downloaded.
FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "files")


def send_dummy_data(conn, total_bytes=1000000):
  """What the server does now: push total_bytes of dummy data, then END.

  TODO (Part 1): replace this with a function that sends the content of a real
  file. Read it chunk by chunk (e.g. f.read(chunkSize)): do not load the whole
  file in memory at once.
  """
  sent = 0
  while sent < total_bytes:
    chunk = b"x" * min(chunkSize, total_bytes - sent)
    send_message(conn, Message(DATA, chunk))
    sent += len(chunk)
  send_message(conn, Message(END))
  
def send_list(conn):
  """Send the list of files in FILES_DIR to the client.

  TODO (Part 1): send a LIST_REPLY message with the names (and sizes) of the
  files in FILES_DIR. See os.listdir and os.path.getsize.
  """
  raise NotImplementedError("send_list is not implemented yet")

def send_file(conn, name):
  """Send the file `name` from FILES_DIR to the client, or an error if it does not exist.

  Returns the number of bytes sent. If the file does not exist, send an ERROR
  message and return None.
  """
  # TODO (Part 1)
  raise NotImplementedError("send_file is not implemented yet")

def handle_client(conn):
  # TODO (Part 1): the server must not push data as soon as the client connects.
  # Instead, it must read the client's requests with recv_message() in a loop and
  # answer each of them:
  #   - a request for the list of files -> reply with the names (and sizes) of
  #     the files in FILES_DIR (see os.listdir and os.path.getsize);
  #   - a request for one file          -> send the file, or an error if it does
  #     not exist. Careful: a client asking for "../apps/server.py" must NOT get it!
  # Stop when recv_message() returns None: the client closed the connection.
  send_dummy_data(conn)


def main():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # Allow restarting the server right away without "Address already in use"
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind((localIP, localPort))
  s.listen(1)
  print(f"Serving {os.path.abspath(FILES_DIR)} on port {localPort}")

  # One client at a time
  while True:
    conn, addr = s.accept()
    print(f"Connection from {addr[0]}:{addr[1]}")
    try:
      handle_client(conn)
    except (ConnectionError, OSError) as e:
      print(f"Connection with {addr[0]}:{addr[1]} failed: {e}")
    finally:
      conn.close()


if __name__ == "__main__":
  main()
