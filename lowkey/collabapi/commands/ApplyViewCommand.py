from lowkey.collabapi.commands.Command import Command


class ApplyViewCommand(Command):

    def __init__(self, params):
        self._params = params

    def execute(self, session):
        print(self._params)
        session.applyView(self._params)
