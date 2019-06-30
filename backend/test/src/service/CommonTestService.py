import os

class CommonTestService(object):

    GLOBAL_TEST_CONFIG = None

    @classmethod
    def load_global_config(cls):
        if cls.GLOBAL_TEST_CONFIG:
            return cls.GLOBAL_TEST_CONFIG
        else:
            cls.GLOBAL_TEST_CONFIG = {
                'MONGO_HOSTNAME' : os.environ.get('MONGO_HOST'),
                'MONGO_PORT' : int(os.environ.get('MONGO_PORT')),
                'MONGO_DB' : os.environ.get('MONGO_DB'),
            }
            return cls.GLOBAL_TEST_CONFIG

