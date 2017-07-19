class NamedEventHook(object):
    '''Observer pattern event hooks'''
    
    def __init__(self):
        self.__handlers = {}
        self.__changed = 0

    def add_handler(self, event_name, handler):
        self.__handlers.setdefault(event_name, []).append(handler)
        return self

    def remove_handler(self, event_name, handler):
        self.__handlers[event_name].remove(handler)
        return self

    def fire(self, event_name, *args, **kwargs):
        '''fires event on all event handlers'''
        if event_name in self.__handlers:
            for handler in self.__handlers[event_name]:
                handler(*args, **kwargs)

    def clear_handlers(self, event_name):
        '''clears all event handlers from this hook'''
        self.__handlers[event_name] = []

    def clear_all_handlers(self):
        self.__handlers = {}

    def count_handlers(self, event_name):
        '''count event handlers'''
        return len(self.__handlers)

    def count_all_handlers(self):
        '''count event handlers'''
        count = 0
        for event in self.__handlers:
            count += len(event)
        return count