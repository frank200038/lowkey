from lowkey.collabapi.commands.Command import Command

class ReadObjectsCommand(Command):
    def execute(self, session):
        root = session.getModels()[0]
        nodes = root.getNodes()

        views = root.getViews()
        viewPoints = root.getViewPoints()


        if nodes:
            for n in nodes:
                print(n.getName(), n)
        else:
            print("No objects in the model yet")

        print("------------------------------------------")
        if views:
            for v in views:
                print(v.getViewName(), v, " Linked To VP: ", v.getViewPointName())
        else:
            print("No views in the model yet")

        print("------------------------------------------")
        if viewPoints:
            for vp in viewPoints:
                print(vp.getViewPointName(), vp, " with types: ", vp.getTypes())
        else:
            print("No view points in the model yet")