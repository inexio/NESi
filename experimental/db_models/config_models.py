from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum, Boolean, FLOAT, Float
from sqlalchemy.ext.declarative import declarative_base as db
from sqlalchemy.orm import sessionmaker, relationship
from nesi.softbox.api import ma


alcatel_base = db()
huawei_base = db()
alcatel_engine = create_engine('sqlite:///alcatel.db')
huawei_engine = create_engine('sqlite:///huawei.db')
Session = sessionmaker()


def add_boxschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls

        subracks = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_subracks', box_id='<id>')}})

        from experimental.interfaces.api_interface.schemas.subrack_schema import SubracksSchema

        subrack_details = ma.Nested(SubracksSchema.SubrackSchema, many=True)

    cls.Schema = Schema
    return cls


def add_subrackschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls

    cls.Schema = Schema
    return cls