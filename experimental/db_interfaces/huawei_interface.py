from ..db_models.huawei_models import *


class HuaweiInterface:

    def __init__(self):
        huawei_base.metadata.create_all(huawei_engine)
        self.session = Session(bind=huawei_engine)

    def store(self, object):
        self.session.add(object)
        self.session.commit()

    def create_box(self, vendor, model):
        box = HuaweiBox(vendor=vendor, model=model)
        self.store(box)

    def get_box_by_id(self, value, multiple=False):
        if multiple is True:
            box = self.session.query(HuaweiBox).filter_by(id=value).all()
        else:
            box = self.session.query(HuaweiBox).filter_by(id=value).one()
        print(box)
        return box

