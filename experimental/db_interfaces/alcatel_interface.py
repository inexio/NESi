from ..db_models.alcatel_models import *
from .base_interface import Interface


class AlcatelInterface(Interface):

    def __init__(self, dropall=False):
        super().__init__()
        if dropall:
            alcatel_base.metadata.drop_all(alcatel_engine)
        alcatel_base.metadata.create_all(alcatel_engine)
        self.session = Session(bind=alcatel_engine)
        self.box_id = None
        self.box = AlcatelBox

    def create_box(self, vendor, model, subracknames):
        box = AlcatelBox(vendor=vendor, model=model)
        subracks = []
        for x in subracknames:
            subrack = AlcatelSubrack(name=x)
            subracks.append(subrack)
        box.subrack = subracks
        box.credentials = [Credentials(username='admin', password='secret')]
        self.store(box)
        self.box_id = box.id

