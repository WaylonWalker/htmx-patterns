from datetime import date, datetime
from typing import List, Union

from faker import Faker
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import UUID4, BaseModel

faker = Faker()


class Person(BaseModel):
    id: UUID4
    name: str
    birthday: Union[datetime, date]
    phone_number: str


class PersonFactory(ModelFactory):
    name = faker.name
    phone_number = faker.phone_number
    __model__ = Person


# result = PersonFactory.build()
