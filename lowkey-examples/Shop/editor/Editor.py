import argparse
import logging
import os
import sys
import threading

from DSLParser import DSLParser
from ShopSession import ShopSession
from lowkey.network.Client import Client

from metamodel.entities.ShopModel import ShopModel

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")


class Editor(Client):
    __encoding = "utf-8"

    def __init__(self):
        super().__init__()
        self._session = ShopSession()
        self._parser = DSLParser()

    def run(self):
        connection_thread = threading.Thread(target=self.subscribe, args=())
        connection_thread.daemon = True
        logging.debug("Starting connection thread")
        connection_thread.start()
        logging.debug("Starting editor")
        self.editorThread()

    def join(self):
        self._snapshot.send(b"request_snapshot")
        while True:
            try:
                receviedMessage = self._snapshot.recv()
                logging.debug("Received message {}".format(receviedMessage))
                _, message = self.getMessage(receviedMessage)
                self.processMessage(message)
            except:
                return

    def subscriberAction(self):
        receviedMessage = self._subscriber.recv()
        senderId, message = self.getMessage(receviedMessage)

        if self.throwawayMessage(senderId):
            logging.debug("Throwing away message from {}".format(senderId))
        else:
            logging.debug("Received message {}".format(message))
            self.processMessage(message)

    def editorThread(self):
        print("Read User Input")
        while True:
            userInput = str(input())
            if not userInput:
                continue

            tokens = self._parser.tokenize(userInput)
            commandKeyWord = tokens[0].upper()
            if self._parser.isLocalCommand(commandKeyWord):
                commandObject = self._parser.processLocalMessage(commandKeyWord)
                commandObject.execute(self._session)
            elif self._parser.isGlobalCommand(commandKeyWord):
                collabAPICommand = self._parser.translateIntoCollabAPICommand(userInput)
                if collabAPICommand is None:
                    print("Something wrong with the command. Please try again!")
                    continue
                self._session.processMessage(collabAPICommand)
                message = self.createMessage(collabAPICommand)
                self._publisher.send(message)
            else:
                print("Invalid command. Please try again!")
                continue

    def createMessage(self, message):
        return bytes('[{}] {}'.format(self._id, message), self.__encoding)

    def getMessage(self, rawMessage):
        return rawMessage.decode(self.__encoding).split(' ', 1)

    def processMessage(self, message):
        self._session.processMessage(message)

    def throwawayMessage(self, senderId):
        return senderId.replace('[', '').replace(']', '') == str(self._id)


if __name__ == "__main__":
    editor = Editor()
    editor.join()
    editor.run()
