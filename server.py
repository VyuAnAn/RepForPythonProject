""" Создать 2 приложения – клиент/сервер (тип связи - любой).
После подключения передать на сервер массив и произвести обработку данных и вернуть на клиент:
Массив: [1, ‘4’, 5, 6, ‘a’, ‘azaza’, 12, 34, 0].
Обработка данных:
1. Необходимо удалить строковые данные.
2. Необходимо отсортировать массив по убыванию/возрастанию.
3. Необходимо найти среднее арифметическое массива и записать в конец. """

import json
import socket
import statistics

HOST = 'localhost'
PORT = 5050
MAX_CONNECTIONS = 5


def get_server_socket():
    """ Запуск сервера, ожидающего подключения """
    # создаем
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # подключаем
    server_socket.bind((HOST, PORT))

    # ожидаем подключение
    server_socket.listen(MAX_CONNECTIONS)
    print('Ожидание подключения....')
    return server_socket


def del_str(data):
    """ Удаление строковых данных """
    return [x for x in data if isinstance(x, int)]


def sort_list(data, reverse=False):
    """ Сортировка массива """
    return sorted(data, reverse=reverse)


def average_list(data):
    """ Среднее арифметическое массива и запись в конец """
    item = int(statistics.mean(data))
    data.append(item)
    return data


server_socket = get_server_socket()

try:
    while True:
        # обработка подключений
        client_socket, client_addr = server_socket.accept()
        print('Соединение с ', client_addr)

        while True:
            # считывание переданных данных
            data = client_socket.recv(1024)

            if not data:
                print('Пользователь {addr} отсоединён'.format(addr=client_addr))
                break

            data = json.loads(data.decode())
            user_list = data.get('list_send')
            print('Данные пользователя {addr} переданные на сервер: {data}'.
                  format(addr=client_addr, data=user_list))

            list_without_str = del_str(user_list)
            print('Список после удаления строковых данных: ', list_without_str)

            sorted_list = sort_list(list_without_str)
            print('Сортировка списка по возрастанию : ', sorted_list)

            reverse_sorted_list = sort_list(list_without_str, True)
            print('Сортировка списка по убыванию : ', reverse_sorted_list)

            av_list = average_list(list_without_str)
            print('Среднее арифметическое:', av_list)

            print('Передача данных пользователю...')

            server_dict = {
                'list_without_str': list_without_str,
                'sorted_list': sorted_list,
                'reverse_sorted_list': reverse_sorted_list,
                'av_list': av_list
            }

            # Ответ пользователю
            server_data = json.dumps(server_dict)
            client_socket.sendto(server_data.encode(), client_addr)

        client_socket.close()

except KeyboardInterrupt:
    server_socket.close()
    print("Сервер остановлен")
