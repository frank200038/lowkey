from lowkey.collabapi.commands.Command import Command


class UpdateViewPointTypeCommand(Command):

    def __init__(self, params):
        self._params = params

    def execute(self, session):
        print(self._params)
        session.updateViewPointType(self._params)
