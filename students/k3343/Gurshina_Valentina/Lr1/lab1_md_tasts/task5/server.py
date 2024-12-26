import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080
grades_data = {}


def process_client_request(client_socket, client_address):
    request = client_socket.recv(1024).decode()
    request_parts = request.split(' ')

    if len(request_parts) >= 3:
        method, path, protocol = request_parts[:3]
        print(f"Получен запрос методом {method} от {client_address}")

        if method == 'GET':
            send_http_response(client_socket, '200 OK', 'Content-Type: text/html', generate_html())
        elif method == 'POST':
            content_length = int(request.split('Content-Length: ')[1].split('\r\n')[0])
            body = request.split('\r\n\r\n', 1)[1]
            while len(body.encode('utf-8')) < content_length:
                body += client_socket.recv(1024).decode()
            post_params = extract_post_parameters(body)
            discipline, grade = post_params.get('discipline', ''), post_params.get('grade', '')
            grades_data[discipline] = grades_data.get(discipline, []) + [grade]
            send_http_response(client_socket, '200 OK', 'Content-Type: text/plain', 'Данные получены!')
        else:
            send_http_response(client_socket, '405 Method Not Allowed', 'Content-Type: text/plain',
                                'This method is not allowed. Try again, please ^.^')
    else:
        send_http_response(client_socket, '400 Bad Request', 'Content-Type: text/plain', 'Failed Request')
    client_socket.close()


def send_http_response(client_socket, status_code, content_type, body_content):
    response = f"""HTTP/1.1 {status_code}
{content_type}
Content-Length: {len(body_content)}

{body_content}"""
    client_socket.sendall(response.encode())


def extract_post_parameters(post_data):
    return {key: value.replace('+', ' ') for key, value in [item.split('=') for item in post_data.split('&')]}










#интегрируем html:
def generate_html():
    rows = ''.join([f"<tr><td>{discipline}</td><td>{','.join(grades)}</td></tr>" for discipline, grades in grades_data.items()])
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Отметки</title>
</head>
<body>
    <h1>Отметки</h1>
    <table border="1">
        <tr><th>Дисциплина</th><th>Отметки</th></tr>
        {rows} #для каждой дисциплины создается строка таблицы
    </table>
</body>
</html>"""


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()
    print(f"Запуск сервера на порту {SERVER_PORT}")
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=process_client_request, args=(client_socket, client_address))
        client_thread.start()
