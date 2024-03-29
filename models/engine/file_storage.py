#!/usr/bin/python3
import json
from os.path import isfile
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return the dictionary __objects."""
        if cls:
            return {
                    k: v
                    for k, v in self.__objects.items()
                    if isinstance(v, cls)}
        return FileStorage.__objects

    def classes(self):
        """returns a dictionary of classes"""
        return {
                'BaseModel': BaseModel,
                'User': User,
                'State': State,
                'City': City,
                'Amenity': Amenity,
                'Place': Place,
                'Review': Review
                }

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        serialized_objects = {}
        for key, obj_instance in FileStorage.__objects.items():
            serialized_objects[key] = obj_instance.to_dict()

        with open(FileStorage.__file_path, 'w', encoding='utf-8') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for key, obj_dict in data.items():
                    class_name, obj_id = key.split('.')
                    class_obj = globals().get(class_name, None)
                    if class_obj:
                        obj_instance = class_obj(**obj_dict)
                        FileStorage.__objects[key] = obj_instance
        except FileNotFoundError:
            pass

    def to_dict(self):
        """Return a dictionary representation of all objects."""
        attributes = {}
        for key, value in FileStorage.__objects.items():
            if hasattr(
                    value,
                    'to_dict') and callable(
                            getattr(value, 'to_dict')):
                attributes[key] = value.to_dict()
        return attributes

    def from_dict(self, obj_dict):
        """Update objects from the dictionary."""
        for key, attributes_dict in obj_dict.items():
            class_name, obj_id = key.split('.')
            class_obj = globals().get(class_name, None)(**attributes_dict)
            FileStorage.__objects[key] = class_obj
        return FileStorage.__objects

    def attributes(self):
        """Return a dictionary with class names and thier attributes."""
        attributes_dict = {}
        for key, value in FileStorage.__objects.items():
            class_name = key.split('.')[0]
            if class_name not in attributes_dict:
                attributes_dict[class_name] = value.to_dict().keys()
        return attributes_dict
