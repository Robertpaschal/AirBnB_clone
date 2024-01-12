#!/usr/bin/python3

import cmd
import json
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def do_create(self, arg):
        """Create a new instance of BaseModel, saves it, and prints the id."""
        args = arg.split()
        if not args or args[0] == "":
            print("** class name missing **")
            return
        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return

        new_instance = cls()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance."""
        args = arg.split()
        if not args or args[0] == "":
            print("** class name missing **")
            return
        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return

        if len(args) < 2 or args[1] == "":
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return

        print(storage.all()[key])

    def do_destory(self, arg):
        """Deletes an instance based on the class name and id."""
        args = arg.split()
        if not args or args[0] == "":
            print("** class name missing **")
            return
        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return

        if len(args) < 2 or args[1] == "":
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return

        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances."""
        args = arg.split()
        obj_list = []
        if not arg or args[0] == "":
            for obj in storage.all().values():
                obj_list.append(str(obj))
            print(obj_list)
            return
        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return

        for key, obj in storage.all().items():
            if args[0] == key.split('.')[0]:
                obj_list.append(str(obj))
        print(obj_list)

    def do_update(self, arg):
        """Updates an instance based on the class name and id."""
        args = arg.split()
        if not args or args[0] == "":
            print("** class name missing **")
            return
        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return

        if len(args) < 2 or args[1] == "":
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
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

        setatrr(storage.all()[key], args[2], value)
        storage.save()

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program."""
        print()
        return True

    def emptyline(self):
        """Do nothing on empty input line."""
        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()
