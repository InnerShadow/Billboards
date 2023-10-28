
from ServerData.Client import *

class User:

    client : Client = Client("127.0.0.1", 2000)

    def __init__(self, login : str, role : str):
        self.login = login
        self.role = role
        self.ip_address = self.client.get_ip_address()
