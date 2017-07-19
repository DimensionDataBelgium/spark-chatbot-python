class Interpreter(object):

    def __init__(self, config):
        self.ignore_self = config.ignore_self
        self.trim_mention = config.trim_mention
        self.command_prefix = config.command_prefix
        #self.__token = config.token
