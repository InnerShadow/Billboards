import socket

class Client:
    def __init__(self, host : str, port : int):
        self.host = host
        self.port = port


    def Get_response(self, request):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.host, self.port))

            client.send(request.encode('utf-8'))

            response = b''
            while True:
                data = client.recv(1024)
                if not data:
                    break
                response += data

            #print(response.decode('utf-8'))
        finally:
            client.close()

        if 'GET AD' in request:
            return response

        else:
            return response.decode('utf-8')
    

    def get_ip_address(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.1)
            
            s.connect(("8.8.8.8", 80))
            local_ip_address = s.getsockname()[0]
            s.close()
            
            return local_ip_address
        except Exception as e:
            print(f"Error getting local IP address: {e}")
            return None
