class Add:

    def __init__(self, *args):
        self.args = args
    
    def execute(self):
        return self.args[0] + self.args[1]