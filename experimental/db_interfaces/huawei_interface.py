from ..db_models.huawei_models import *
from .base_interface import Interface


class HuaweiInterface(Interface):

    def __init__(self, dropall=False):
        super().__init__()
        if dropall:
            huawei_base.metadata.drop_all(huawei_engine)
        huawei_base.metadata.create_all(huawei_engine)
        self.session = Session(bind=huawei_engine)
        self.box_id = None
        self.box = HuaweiBox

    def create_box(self, vendor, model, subracknames):
        box = HuaweiBox(vendor=vendor, model=model)
        box.credentials = [Credentials(username='admin', password='secret')]
        self.store(box)
        self.box_id = box.id

