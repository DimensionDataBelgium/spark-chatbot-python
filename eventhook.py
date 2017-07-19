class EventHook(object):
    '''Observer pattern event hooks'''
    
    def __init__(self):
        self.__handlers = set()
        self.__changed = 0

    def add_handler(self, handler):
        self.__handlers.add(handler)
        return self

    def remove_handler(self, handler):
        try:
            self.__handlers.remove(handler)
        except:
            raise ValueError("Handler is not handling this event, so cannot unhandle it.")
        return self

    def fire(self, *args, **kwargs):
        '''fires event on all event handlers'''
        for handler in self.__handlers:
            handler(*args, **kwargs)

    def clear_handlers(self):
        '''clears all event handlers from this hook'''
        self.__handlers = set()

    def count_handlers(self):
        '''count event handlers'''
        return len(self.__handlers)

    __iadd__ = add_handler
    __isub__ = remove_handler
    __call__ = fire
    __len__ = count_handlers
