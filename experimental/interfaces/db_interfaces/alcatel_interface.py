from experimental.db_models.alcatel.alcatel_models import *
from .base_interface import Interface


class AlcatelInterface(Interface):

    def __init__(self, box_id=None, dropall=False):
        super().__init__()
        if dropall:
            alcatel_base.metadata.drop_all(alcatel_engine)
        alcatel_base.metadata.create_all(alcatel_engine)
        self.session = Session(bind=alcatel_engine)
        self.box_id = box_id
        self.box = AlcatelBox

    def create_box(self, vendor, model):
        box = AlcatelBox(vendor=vendor, model=model)
        box.credentials = [AlcatelCredentials(username='admin', password='secret')]
        self.store(box)
        self.box_id = box.id
