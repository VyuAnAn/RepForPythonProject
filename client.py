import json
import socket

HOST = 'localhost'
PORT = 5050
list_send = [1, '4', 5, 6, 'a', 'azaza', 12, 34, 0]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Подключение...')
try:
    client_socket.connect((HOST, PORT))

    print('Отправка данных на сервер:', list_send)
    data = json.dumps({'list_send': list_send})
    client_socket.send(data.encode())

    server_data = client_socket.recv(4096)
    print('Данные с сервера:')
    server_data = json.loads(server_data.decode())

    print('Список после удаления строковых данных: ', server_data.get('list_without_str'))
    print('Сортировка списка по возрастанию : ', server_data.get('sorted_list'))
    print('Сортировка списка по убыванию : ', server_data.get('reverse_sorted_list'))
    print('Среднее арифметическое:', server_data.get('av_list'))
finally:
    # закрываем соединение
    print('Данные переданы/получены, соединение закрыто')
    client_socket.close()