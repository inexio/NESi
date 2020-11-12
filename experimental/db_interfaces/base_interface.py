

class Interface:

    def __init__(self, dropall=False):
        self.session = None
        self.box_id = None
        self.box = None

    def store(self, objects):
        self.session.add(objects)
        self.session.commit()

    def create_box(self, vendor, model, subracknames):
        return None

    def get_box(self, value=None, multiple=False):
        if multiple is True:
            box = self.session.query(self.box).all()
        elif value is not None:
            box = self.session.query(self.box).filter_by(id=value).first()
        else:
            box = self.session.query(self.box).filter_by(id=self.box_id).first()
        return box

    def check_credentials(self, username, password):
        box = self.session.query(self.box).filter_by(id=self.box_id).one()
        for cred in box.credentials:
            if cred.username == username and cred.password == password:
                return True
        return False
