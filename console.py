#!/usr/bin/python3


"""Uses the cmd command module to run a simpel console for the project"""

import cmd
import json
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    classes = {
            'BaseModel': BaseModel,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Place': Place,
            'Review': Review,
            'User': User
    }

    def do_create(self, arg):
        """Create a new instance of BaseModel, saves it, and prints the id."""
        args = arg.split()
        if not args or args[0] == "":
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        new_instance = HBNBCommand.classes[class_name]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance."""
        args = arg.split()
        if not args or args[0] == "":
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2 or args[1] == "":
            print("** instance id missing **")
            return

        obj_id = args[1]
        key = "{}.{}".format(args[0], obj_id)
        objects = FileStorage().all()

        if key not in objects:
            print("** no instance found **")
            return

        print(objects[key])

    def do_destory(self, arg):
        """Deletes an instance based on the class name and id."""
        args = arg.split()
        if not args or args[0] == "":
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2 or args[1] == "":
            print("** instance id missing **")
            return

        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        objects = FileStorage().all()

        if key not in objects:
            print("** no instance found **")
            return

        del objects[key]
        FileStorage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances."""
        args = arg.split()
        objects = FileStorage().all()

        if not arg:
            print([str(obj) for obj in objects.values()])
            return

        class_name = args[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        for key, obj in objects.items():
            if class_name == key.split('.')[0]:
                obj_list.append(str(obj))
        print(obj_list)

    def do_update(self, arg):
        """Updates an instance based on the class name and id."""
        args = arg.split()
        if not args or args[0] == "":
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2 or args[1] == "":
            print("** instance id missing **")
            return

        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        objects = FileStorage().all()

        if key not in objects:
            print("** no instance found **")
            return

        if len(args) < 3 or args[2] == "":
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        if args[2] not in obj.__dict__:
            print("** attribute doesn't exist **")
            return

        try:
            value = eval(args[3])
        except (NameError, SyntaxError):
            print("** value missing **")
            return

        setatrr(objects[key], args[2], value)
        storage.save()

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program."""
        print()
        return True

    def emptyline(self):
        """Do nothing on empty input line."""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
