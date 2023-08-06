import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '../../../../Downloads/УаЃ™ 4. Па®ђ•а ѓа†™в®з•б™Ѓ£Ѓ І†§†≠®п'))
from constantsnutils import constants
import client

class TestClass(unittest.TestCase):
    def test_def_presense(self):
        test = client.client_presence()
        test[constants.TIME] = 1.1
        self.assertEqual(test, {constants.ACTION: constants.PRESENCE, constants.TIME: 1.1, constants.USER: {
            constants.ACCOUNT_NAME: 'Guest'}})

    def test_200_ans(self):
        self.assertEqual(client.process_answer({constants.RESPONSE: 200}), '200 : OK')

    def test_400_ans(self):
        self.assertEqual(client.process_answer({constants.RESPONSE: 400, constants.ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        self.assertRaises(ValueError, client.process_answer, {constants.ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
