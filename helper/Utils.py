import inspect

class Utils:

    @staticmethod
    def inspect(obj_or_class):
        """
        Print a structured diagnosis of an object's or class's members and functions.
        Dispatches to a private static handler for each type.
        """
        print("=" * 30)
        print(f"Diagnose for: {type(obj_or_class).__name__}")
        Utils.__dispatch_to_handler(obj_or_class)
        print("=" * 30)

    @staticmethod
    def __dispatch_to_handler(obj):
        if obj is None:
            Utils.__handle_none(obj)
        elif isinstance(obj, dict):
            Utils.__handle_dict(obj)
        elif isinstance(obj, (list, tuple, set)):
            Utils.__handle_collection(obj)
        elif isinstance(obj, (str, int, float, bool)):
            Utils.__handle_primitive(obj)
        else:
            Utils.__handle_object_or_class(obj)

    @staticmethod
    def __handle_none(obj):
        print("(NoneType)")

    @staticmethod
    def __handle_primitive(obj):
        print(f"Value: {repr(obj)}")

    @staticmethod
    def __handle_dict(obj):
        if obj:
            print("(dict)")
            print(f"Length: {len(obj)}")
            print("Keys and sample values:")
            for i, (k, v) in enumerate(obj.items()):
                key_type = type(k).__name__
                val_type = type(v).__name__
                print(f"  [{repr(k)}] ({key_type}): {repr(v)} ({val_type})")
                if i >= 9:
                    print("  ...")
                    break
        else:
            print("(empty dict)")

    @staticmethod
    def __handle_collection(obj):
        tname = type(obj).__name__
        print(f"({tname}) Length: {len(obj)}")
        seq = list(obj)
        if seq:
            print("Sample items:")
            for idx, item in enumerate(seq[:10]):
                print(f"  [{idx}]: {repr(item)} ({type(item).__name__})")
            if len(seq) > 10:
                print("  ...")
        else:
            print(f"(empty {tname})")

    @staticmethod
    def __handle_object_or_class(obj_or_class):
        cls = obj_or_class if inspect.isclass(obj_or_class) else obj_or_class.__class__
        print(f"(class: {cls.__name__})")
        # Instance variables
        if not inspect.isclass(obj_or_class):
            attrs = vars(obj_or_class)
            if attrs:
                print("\nInstance attributes:")
                for name, value in attrs.items():
                    print(f"  {name} = {repr(value)}")
            else:
                print("\nNo instance attributes.")
        else:
            print("\nSkipped instance attributes (input is a class).")
        # Class variables
        class_vars = {k: v for k, v in cls.__dict__.items()
                      if not (k.startswith('__') and k.endswith('__'))
                      and not inspect.isroutine(v)}
        if class_vars:
            print("\nClass attributes:")
            for name, value in class_vars.items():
                print(f"  {name} = {repr(value)}")
        else:
            print("\nNo class attributes.")
        # Methods
        methods = inspect.getmembers(cls, predicate=inspect.isfunction)
        if methods:
            print("\nMethods:")
            for name, func in methods:
                if name.startswith('__') and name.endswith('__'):
                    kind = " (dunder)"
                elif name.startswith('_'):
                    kind = " (private/protected)"
                else:
                    kind = ""
                print(f"  {name}{kind}")
        else:
            print("\nNo methods found.")