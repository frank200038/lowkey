from lowkey.collabapi.commands.Command import Command


class AddViewPointCommand(Command):

    def __init__(self, params):
        self._params = params

    def execute(self, session):
        print(self._params)
        session.createViewPoint(self._params)
