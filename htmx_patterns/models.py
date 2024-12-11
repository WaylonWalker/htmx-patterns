from datetime import datetime
from typing import Optional

from faker import Faker
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import UUID4
from sqlmodel import Field, SQLModel

faker = Faker()


class PersonBase(SQLModel, table=False):
    id: UUID4
    name: str
    birthday: datetime
    phone_number: str

    def get_by_id(session, id):
        return session.get(Person, id)

    def save(self, session):
        session.add(self)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session):
        session.delete(self)
        session.commit()
        return self

    def update(self, session):
        session.merge(self)
        session.commit()
        session.refresh(self)
        return self

    def all(session):
        return session.query(Person).all()

    def paginate(session, page=1, page_size=10):
        return session.query(Person).offset((page - 1) * page_size).limit(page_size)


class Person(PersonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class PersonCreate(PersonBase):
    pass


class PersonRead(PersonBase):
    id: int = Field(default=None, primary_key=True)


class PersonFactory(ModelFactory):
    name = faker.name
    phone_number = faker.phone_number
    __model__ = Person
