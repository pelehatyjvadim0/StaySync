from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

class Model(MappedAsDataclass, DeclarativeBase):
    pass