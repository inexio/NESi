from experimental.db_models.huawei.huawei_models import *
from .base_interface import Interface


class HuaweiInterface(Interface):

    def __init__(self, box_id=None, dropall=False):
        super().__init__()
        if dropall:
            huawei_base.metadata.drop_all(huawei_engine)
        huawei_base.metadata.create_all(huawei_engine)
        self.session = Session(bind=huawei_engine)
        self.box_id = box_id
        self.box = HuaweiBox

    def create_box(self, vendor, model):
        box = HuaweiBox(vendor=vendor, model=model)
        box.credentials = [HuaweiCredentials(username='admin', password='secret')]
        self.store(box)
        self.box_id = box.id

