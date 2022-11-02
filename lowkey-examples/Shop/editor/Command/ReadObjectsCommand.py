from lowkey.collabapi.commands.Command import Command

class ReadObjectsCommand(Command):
    def execute(self, session):
        root = session.getModels()[0]
        nodes = root.getNodes()

        if nodes:
            for n in nodes:
                print(n.getName(), n)
        else:
            print("No objects in the model yet")