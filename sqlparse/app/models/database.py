from orm import Model

class Database(Model):
    id = int
    user = str
    pass = str
    host = str
    script = str
    status = str

    def __init__(self, user,pass,host,script,status):
        self.user = user
        self.pass = pass
        self.host = host
        self.script = script
        self.status = status