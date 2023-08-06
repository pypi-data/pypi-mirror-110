# MongoMapper

Mongo ODM in Python.

MongoMapper is an easy to use ODM for MongoDB, written on top of Pydantic for data validation. Most importantly, it supports `datetime.time` out-of-the-box because for some reason not even the official MongoDB library supports it. Do coders hate dates that much?

## Install
```
pip install mongomapper
```

## Quick start

### Schemas

```python
# examples/schemas.py
from mongomapper import Schema

class User(Schema):
  __collection_name__ = 'users'

  name: str

doc = User.create(name="John")

print(doc.data)
```

### References

```python
# examples/references.py
from mongomapper import Schema, Reference

class Person(Schema):
  __collection_name__ = 'people'

  name: str

class Phone(Schema):
  __collection_name__ = 'phones'

  owner: Reference(Person)

person = Person.create(name="John")
phone = Phone.create(owner=person)

print(person.data)
print(phone.data)
```