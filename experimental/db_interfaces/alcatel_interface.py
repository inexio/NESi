from ..db_models.alcatel_models import *


class AlcatelInterface:

    def __init__(self):
        alcatel_base.metadata.create_all(alcatel_engine)
        self.session = Session(bind=alcatel_engine)

    def store(self, objects):
        self.session.add(objects)
        self.session.commit()

    def create_box(self, vendor, model, subracknames):
        box = AlcatelBox(vendor=vendor, model=model)
        subracks = []
        for x in subracknames:
            subrack = AlcatelSubrack(name=x)
            subracks.append(subrack)
        box.subrack = subracks
        self.store(box)

    def get_box_by_id(self, value, multiple=False):
        if multiple is True:
            box = self.session.query(AlcatelBox).all()
        else:
            box = self.session.query(AlcatelBox).filter_by(id=value).one()
        print(box)
        return box

