from datetime import datetime

class Log:
    LOG_TYPE_INFO = 'INFO'
    LOG_TYPE_ERROR = 'ERROR'

    def __print_messages(type, messages):
        for message in messages:
            print('%s  %s: %s' % (datetime.utcnow(), type, str(message)))

    @classmethod
    def info(cls, *messages):
        cls.__print_messages(cls.LOG_TYPE_INFO, messages)

    @classmethod
    def err(cls, *messages):
        cls.__print_messages(cls.LOG_TYPE_ERROR, messages)
