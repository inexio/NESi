

class Interface:

    def __init__(self, dropall=False):
        self.session = None
        self.box_id = None
        self.box = None

    def store(self, objects):
        self.session.add(objects)
        self.session.commit()

    def delete(self, box_id, objects):
        self.session.delete(objects)
        self.session.commit()
        box = self.get_box(box_id)
        box.collect_subcomponents()
        self.session.add(box)
        self.session.commit()

    def close_session(self):
        self.session.close()

    def create_box(self, vendor, model):
        return None

    def get_box(self, value=None, multiple=False):
        if multiple is True:
            box = self.session.query(self.box).all()
        elif value is not None:
            box = self.session.query(self.box).filter_by(id=value).first()
        else:
            box = self.session.query(self.box).filter_by(id=self.box_id).first()
        return box