import os
import socket
from http import HTTPStatus

ADDRESS = ('127.0.0.1', 2000)


def main():
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0) as sock:
        print(f'Server started on {ADDRESS[0]}:{ADDRESS[1]}, pid: {os.getpid()}')
        sock.bind(ADDRESS)
        sock.listen(1)

        while True:
            print('Wait for client connection...')
            conn, radd = sock.accept()
            print(f'Connection from {radd}')
            while True:
                response = conn.recv(1024)
                text = response.decode('utf-8')

                method = text.split(' /')[0]
                headers_from_requst = text.split('\r\n')[1:]
                sub_str_with_status = text.split('\r\n')[0]
                try:
                    status_from_request = int(sub_str_with_status.split(' ')[1].split('status=')[1])
                    status = HTTPStatus(status_from_request)
                except:
                    status = HTTPStatus(200)

                started_line = f'HTTP/1.1 {status.value} {status.name}'
                headers = '\r\n'.join(headers_from_requst)

                message = f'{started_line}\r\n\r\n' \
                          f'\nRequest Method: {method}' \
                          f'\nRequest Source: {radd}' \
                          f'\nResponse Status: {status.value} {status.name}' \
                          f'\r\n' \
                          f'\n{headers}'.encode('utf-8')

                conn.send(message)
                conn.close()
                break


if __name__ == '__main__':
    main()
