import socket

class Client:
    #Init socket data
    def __init__(self, host : str, port : int):
        self.host = host
        self.port = port


    #Get abd decode response
    def Get_response(self, request : str):
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

        finally:
            client.close()

        #Do not decode in we ask about video
        if 'GET AD' in request:
            return response

        else:
            return response.decode('utf-8')


    #Set video helper
    def Send_ad(self, video_name: str, video_url: str):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.host, self.port))

            request = f"UPLOAD FILE file_name = {video_name}"
            client.send(request.encode('utf-8'))

            with open(video_url, 'rb') as video_file:
                while True:
                    chunk = video_file.read(1024)
                    if not chunk:
                        break
                    client.send(chunk)

        finally:
            client.close()
            return "File uploaded successfully"


    #Get local ip address
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

