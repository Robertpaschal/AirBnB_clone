#!/usr/bin/python3
'''
    Base model where common attributes and methods are defined
'''
import uuid
from datetime import datetime


class BaseModel:
    def __init__(self, *args, **kwargs):
        """Initialize BaseModel instance."""
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        value = datetime.strptime(
                                value,
                                "%Y-%m-%dT%H:%M:%S.%f"
                            )
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            from models import storage
            storage.new(self)

    def __str__(self):
        """Return a string representation of the object."""
        return "[{}] ({}) {}".format(
                self.__class__.__name__,
                self.id,
                self.__dict__
                )

    def save(self):
        """Update the public instance attribute with the current datetime"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        Return a dictionary containing all keys/values of the instance.
        Keys:
        - __class__: Class name of the object
        - created_at: Converted to string in ISO format
        - updated_at: Converted to string in ISO format
        """
        obj_dict = {}
        for key, value in self.__dict__.items():
            obj_dict[key] = value

        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict

    def from_dict(self, d):
        """Update attributes from the dictionary."""
        if '__class__' in d:
            del d['__class__']
        d['created_at'] = datetime.strptime(
                d['created_at'],
                "%Y-%m-%dT%H:%M:%S.%f"
            )
        d['updated_at'] = datetime.strptime(
                d['updated_at'],
                "%Y-%m-%dT%H:%M:%S.%f"
                )
        return d
