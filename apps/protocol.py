import struct

# Message types. Every message starts with its type (1 byte).
DATA = 0  # a chunk of data: the payload is the raw bytes
END = 1   # the sender has no more data to send: empty payload

# TODO (Part 1): add the message types your protocol needs, for example:
#   LIST        client -> server, "which files do you have?"
#   LIST_REPLY  server -> client, the list of files
#   GET         client -> server, "send me this file" (the payload is the file name)
#   ERROR       server -> client, something went wrong (e.g. the file does not exist)
# Choose them yourself, and describe them in the notebook.

# Binary header, in network byte order:
#   | type (1 byte, unsigned) | payload length L (4 bytes, unsigned) | L bytes of payload |
HEADER = struct.Struct("!BI")


class Message:
  """A message as transmitted over the network between client and server."""

  def __init__(self, t, payload=b"") -> None:
    self.t = t              # one of the message types above
    self.payload = payload  # always bytes: encode strings before building a message

  def encode(self):
    return HEADER.pack(self.t, len(self.payload)) + self.payload

  def __repr__(self):
    return f"Message(t={self.t}, {len(self.payload)} bytes of payload)"


def send_message(sock, msg):
  sock.sendall(msg.encode())


def recv_exact(sock, n):
  """Read exactly n bytes from sock.

  TCP is a byte stream: one recv() may return only part of a message, or the
  end of one message and the beginning of the next. So we loop until we have
  exactly the n bytes we want. Returns None if the peer closes the connection
  before sending them.
  """
  data = bytearray()
  while len(data) < n:
    chunk = sock.recv(n - len(data))
    if not chunk:
      return None
    data += chunk
  return bytes(data)


def recv_message(sock):
  """Read the next full message from sock. Returns None if the connection was closed."""
  header = recv_exact(sock, HEADER.size)
  if header is None:
    return None
  t, length = HEADER.unpack(header)
  payload = recv_exact(sock, length)
  if payload is None:
    return None
  return Message(t, payload)
