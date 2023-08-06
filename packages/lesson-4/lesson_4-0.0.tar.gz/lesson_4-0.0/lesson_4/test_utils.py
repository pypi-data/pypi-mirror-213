"""Unit-тесты утилит"""

import sys
import os
import unittest
import json
sys.path.append(os.path.join(os.getcwd(), '../../../../Downloads/УаЃ™ 4. Па®ђ•а ѓа†™в®з•б™Ѓ£Ѓ І†§†≠®п'))
from constantsnutils import constants, utils

class TestSocket:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.receved_message = None

    def send(self, message_to_send):
        """
        Тестовая функция отправки, корретно  кодирует сообщение,
        так-же сохраняет что должно было отправлено в сокет.
        message_to_send - то, что отправляем в сокет
        :param message_to_send:
        :return:
        """
        json_test_message = json.dumps(self.test_dict)
        # кодирует сообщение
        self.encoded_message = json_test_message.encode(constants.ENCODING)
        # сохраняем что должно было отправлено в сокет
        self.receved_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(constants.ENCODING)


class Tests(unittest.TestCase):
    '''
    Тестовый класс, собственно выполняющий тестирование.
    '''
    test_dict_send = {
        constants.ACTION: constants.PRESENCE,
        constants.TIME: 111111.111111,
        constants.USER: {
            constants.ACCOUNT_NAME: 'test_test'
        }
    }
    test_dict_recv_ok = {constants.RESPONSE: 200}
    test_dict_recv_err = {
        constants.RESPONSE: 400,
        constants.ERROR: 'Bad Request'
    }

    def test_send_message(self):
        """
        Тестируем корректность работы фукции отправки,
        создадим тестовый сокет и проверим корректность отправки словаря
        :return:
        """
        # экземпляр тестового словаря, хранит собственно тестовый словарь
        test_socket = TestSocket(self.test_dict_send)
        # вызов тестируемой функции, результаты будут сохранены в тестовом сокете
        utils.send_message(test_socket, self.test_dict_send)
        # проверка корретности кодирования словаря.
        # сравниваем результат довренного кодирования и результат от тестируемой функции
        self.assertEqual(test_socket.encoded_message, test_socket.receved_message)
        # дополнительно, проверим генерацию исключения, при не словаре на входе.
        with self.assertRaises(Exception):
            utils.send_message(test_socket, test_socket)

    def test_make_message(self):
        """
        Тест функции приёма сообщения
        :return:
        """
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        test_sock_err = TestSocket(self.test_dict_recv_err)
        # тест корректной расшифровки корректного словаря
        self.assertEqual(utils.make_message(test_sock_ok), self.test_dict_recv_ok)
        # тест корректной расшифровки ошибочного словаря
        self.assertEqual(utils.make_message(test_sock_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
