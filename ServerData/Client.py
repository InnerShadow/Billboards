import socket

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port


    def send_number_to_server(self, number):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.host, self.port))

            client.send(str(number).encode('utf-8'))

            response = b''
            while True:
                data = client.recv(1024)
                if not data:
                    break
                response += data

            print(response.decode('utf-8'))
        finally:
            client.close()

