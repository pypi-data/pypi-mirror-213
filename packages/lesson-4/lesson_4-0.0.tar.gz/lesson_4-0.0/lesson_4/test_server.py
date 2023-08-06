import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '../../../../Downloads/УаЃ™ 4. Па®ђ•а ѓа†™в®з•б™Ѓ£Ѓ І†§†≠®п'))
from constantsnutils import constants
import server

class TestServer(unittest.TestCase):
    err_dict = {
        constants.RESPONSE: 400,
        constants.ERROR: 'Bad Request'
    }
    ok_dict = {constants.RESPONSE: 200}

    def test_no_action(self):
        self.assertEqual(server.process_client_message(
            {constants.TIME: '1.1', constants.USER: {constants.ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_wrong_action(self):
        self.assertEqual(server.process_client_message(
            {constants.ACTION: 'Wrong', constants.TIME: '1.1', constants.USER: {constants.ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_time(self):
        self.assertEqual(server.process_client_message(
            {constants.ACTION: constants.PRESENCE, constants.USER: {constants.ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        self.assertEqual(server.process_client_message(
            {constants.ACTION: constants.PRESENCE, constants.TIME: '1.1'}), self.err_dict)

    def test_unknown_user(self):
        self.assertEqual(server.process_client_message(
            {constants.ACTION: constants.PRESENCE, constants.TIME: 1.1, constants.USER: {
                constants.ACCOUNT_NAME: 'Guest1'}}), self.err_dict)

    def test_ok_check(self):
        self.assertEqual(server.process_client_message(
            {constants.ACTION: constants.PRESENCE, constants.TIME: 1.1, constants.USER: {
                constants.ACCOUNT_NAME: 'Guest'}}), self.ok_dict)


if __name__ == '__main__':
    unittest.main()
