import socket

def send_number_to_server(number):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 2000))

        # Отправляем число на сервер
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

if __name__ == '__main__':
    number = 5
    send_number_to_server(number)

