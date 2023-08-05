class iptools():
  def getIP():
    import socket
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address
  def helloWorld():
    print("Hell0 W0rld")