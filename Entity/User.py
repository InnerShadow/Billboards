
from ServerData.Client import Client

#Simple user container
class User:
    client : Client = Client("192.168.1.106", 2000)

    def __init__(self, login : str = None, role : str = None):
        self.login = login
        self.role = role
        self.ip_address = self.client.get_ip_address()

