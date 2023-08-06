import unittest
from QuantumPathQSOAPySDK import QSOAPlatform


##################_____ENCODE PASSWORD_____##################
class Test_EncodePassword(unittest.TestCase):

    # ENCODE PASSWORD
    def test_encodePassword(self):
        qsoa = QSOAPlatform()

        encodedPassword = qsoa.encodePassword('password')

        self.assertEqual(encodedPassword, 'cGFzc3dvcmQ=')

    # BAD ARGUMENT TYPE password
    def test_encodePassword_badArgumentType_password(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.encodePassword(99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____ENCRYPT PASSWORD_____##################
class Test_EncryptPassword(unittest.TestCase):

    # ENCRYPT PASSWORD
    def test_encryptPassword(self):
        qsoa = QSOAPlatform()

        encryptedPassword = qsoa.encryptPassword('password')

        self.assertEqual(encryptedPassword, '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8')

    # BAD ARGUMENT TYPE password
    def test_encryptPassword_badArgumentType_password(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.encryptPassword(99)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____AUTHENTICATE BASIC_____##################
class Test_AuthenticateBasic(unittest.TestCase):

    '''
    INTRODUCE MANUALLY USERNAME AND PASSWORD
    '''
    # AUTHENTICATEBASIC
    # def test_authenticateBasic(self):
    #     qsoa = QSOAPlatform()

    #     username = 'username'
    #     password = 'password'

    #     authenticated = qsoa.authenticate(username, password)

    #     self.assertTrue(authenticated)

    '''
    INTRODUCE MANUALLY BAD USERNAME AND GOOD PASSWORD
    '''
    # AUTHENTICATEBASIC BAD ARGUMENT username
    # def test_authenticateBasic_badArgument_username(self):
    #     qsoa = QSOAPlatform()

    #     username = 'username'
    #     password = 'password'

    #     try:
    #         qsoa.authenticate(username, password)
    #         raise Exception

    #     except Exception as e:
    #         self.assertEqual(type(e).__name__, 'APIConnectionError')

    '''
    INTRODUCE MANUALLY GOOD USERNAME AND BAD PASSWORD
    '''
    # AUTHENTICATEBASIC BAD ARGUMENT password
    # def test_authenticateBasic_badArgument_password(self):
    #     qsoa = QSOAPlatform()

    #     username = 'username'
    #     password = 'password'

    #     try:
    #         qsoa.authenticate(username, password)
    #         raise Exception

    #     except Exception as e:
    #         self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE username
    def test_authenticateBasic_badArgumentType_username(self):
        qsoa = QSOAPlatform()

        username = 99
        password = 'password'

        try:
            qsoa.authenticate(username, password)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE password
    def test_authenticateBasic_badArgumentType_password(self):
        qsoa = QSOAPlatform()

        username = 'username'
        password = 99

        try:
            qsoa.authenticate(username, password)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____AUTHENTICATE_____##################
class Test_Authenticate(unittest.TestCase):

    '''
    INTRODUCE MANUALLY USERNAME AND PASSWORD
    '''
    # AUTHENTICATE MANUALLY
    # def test_authenticate_manually(self):
    #     qsoa = QSOAPlatform()

    #     username = 'username'
    #     password = 'password' # password encoded in Base64

    #     authenticated = qsoa.authenticate(username, password)

    #     self.assertTrue(authenticated)

    '''
    CREATE .QPATH CONFIG FILE
    '''
    # AUTHENTICATE CONFIG FILE
    # def test_authenticate_configFile(self):
    #     qsoa = QSOAPlatform()

    #     authenticated = qsoa.authenticate()

    #     self.assertTrue(authenticated)

    # AUTHENTICATE USER MANUALLY BAD ARGUMENT username password
    def test_authenticate_manually_badArgument_username_password(self):
        qsoa = QSOAPlatform()

        username = 'username'
        password = 'cGFzc3dvcmQ=' # password encoded in Base64

        try:
            qsoa.authenticate(username, password)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT password BASE64
    def test_authenticate_badArgument_password_base64(self):
        qsoa = QSOAPlatform()

        username = 'username'
        password = 'password'

        try:
            qsoa.authenticate(username, password)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'Base64Error')

    # BAD ARGUMENT TYPE username
    def test_authenticate_badArgumentType_username(self):
        qsoa = QSOAPlatform()

        username = 99
        password = 'password'

        try:
            qsoa.authenticate(username, password)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE password
    def test_authenticate_badArgumentType_password(self):
        qsoa = QSOAPlatform()

        username = 'username'
        password = 99

        try:
            qsoa.authenticate(username, password)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____AUTHENTICATEEX_____##################
class Test_AuthenticateEx(unittest.TestCase):

    '''
    INTRODUCE MANUALLY USERNAME AND PASSWORD
    '''
    # AUTHENTICATE MANUALLY
    # def test_authenticateEx_manually(self):
    #     qsoa = QSOAPlatform()

    #     username = 'username'
    #     password = 'password' # password encrypted in SHA-256

    #     authenticated = qsoa.authenticateEx(username, password)

    #     self.assertTrue(authenticated)

    '''
    CREATE .QPATH CONFIG FILE
    '''
    # AUTHENTICATE CONFIG FILE
    # def test_authenticateEx_configFile(self):
    #     qsoa = QSOAPlatform()

    #     authenticated = qsoa.authenticateEx()

    #     self.assertTrue(authenticated)

    # AUTHENTICATE USER MANUALLY BAD CREDENTIALS
    def test_authenticateEx_manually_badArgument_username_password(self):
        qsoa = QSOAPlatform()

        username = 'username'
        password = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8' # password encrypted in SHA-256

        try:
            qsoa.authenticateEx(username, password)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'APIConnectionError')

    # BAD ARGUMENT TYPE username
    def test_authenticateEx_badArgumentType_username(self):
        qsoa = QSOAPlatform()

        username = 99
        password = 'password'

        try:
            qsoa.authenticateEx(username, password)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE password
    def test_authenticateEx_badArgumentType_password(self):
        qsoa = QSOAPlatform()

        username = 'username'
        password = 99

        try:
            qsoa.authenticateEx(username, password)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____ECHOPING_____##################
class Test_Echoping(unittest.TestCase):

    # ECHOPING
    def test_echoping(self):
        qsoa = QSOAPlatform()

        ping = qsoa.echoping()

        self.assertIsInstance(ping, bool)


##################_____ECHOSTATUS_____##################
class Test_Echostatus(unittest.TestCase):

    # ECHOSTATUS
    def test_echostatus(self):
        qsoa = QSOAPlatform()

        status = qsoa.echostatus()

        self.assertIsInstance(status, bool)


##################_____ECHOUSER_____##################
class Test_Echouser(unittest.TestCase):

    # ECHOUSER
    def test_echouser(self):
        qsoa = QSOAPlatform(configFile=True)

        login = qsoa.echouser()

        self.assertIsInstance(login, str)


if __name__ == '__main__':
    unittest.main()