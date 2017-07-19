'''Util/EventHook.py
Module
'''
from ciscosparkapi import CiscoSparkAPI, Webhook
from eventhook import EventHook
from namedeventhook import NamedEventHook
import asyncio


class Chatbot(object):
    '''Observer pattern event hooks'''
  
    def __init__(self, token):
        self.__token = token
        self.__api = CiscoSparkAPI(access_token=token)
        self.ignore_self = 1
        self.bot_id = self.get_id()
        self.on_message = EventHook()
        self.on_command = NamedEventHook()
        self.on_event = NamedEventHook()
        #self.__loop = asyncio.get_event_loop()
        


    def get_id(self):
        bot_id = self.__api.people.me().id
        return bot_id

    def reply(self, hook: Webhook, message):
        self.__api.messages.create(hook.data.roomId, text=message)

    def get_message(self, hook: Webhook):
        message = self.__api.messages.get(hook.data.id)
        return message.text
    
    def send_message(self, room, message):
        pass

    

    def on_hook(self, hook):
        # TODO check for Message to bot
        # TODO check for Command
        # if any of the above fire the correct trigger
        number = 0
        if hook.resource == "messages" and hook.event == "created":
            if self.ignore_self and hook.data.personId == self.bot_id:
                pass
            else:
                self.on_message.fire(hook)
        
        event_name = hook.resource + '/' + hook.event
        self.on_event.fire(event_name, hook)

        #self.__loop.run_until_complete(main())
