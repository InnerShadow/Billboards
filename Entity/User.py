
from ServerData.Client import *

class User:

    client = Client("127.0.0.1", 2000)

    def __init__(self, login, role):
        self.login = login
        self.role = role
        self.ip_address = self.client.get_ip_address()

