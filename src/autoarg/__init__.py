from functools import wraps
from .arg_handler import ArgsHandler
from .env import ArgEnv, getdefault


def handle_f(f=None, reserved_args: dict = None, arg_env: ArgEnv = None):
    def wrapper(f):
        nonlocal reserved_args, arg_env
        if not arg_env:
            arg_env = ArgEnv(reserved_args) if reserved_args else getdefault()
        args_handler = ArgsHandler(f, arg_env.args)

        @wraps(f)
        def wrapped(*args, **kwds):
            args, kwds = args_handler.parse_args(args, kwds)
            return f(*args, **kwds)

        return wrapped

    if f:
        return wrapper(f)
    return wrapper


def handle_method(instance, f, reserved_args: dict = None, arg_env: ArgEnv = None):
    try:
        method = getattr(instance, f)
        wrapped_method = handle_f(method, reserved_args, arg_env)
        setattr(instance, method.__name__, wrapped_method)
    except AttributeError as exc:
        raise exc


def handle_instance(
    instance,
    reserved_args: dict = None,
    arg_env: ArgEnv = None,
    on_names: list = None,
    strict: bool = True,
):
    attrs = dir(instance)

    if on_names:
        for method in on_names:
            if _check_attr(method, attrs, strict):
                handle_method(instance, method, reserved_args, arg_env)
        return instance

    no_magic_attrs = [
        attr for attr in attrs if not (attr.startswith("__") and attr.endswith("__"))
    ]
    for method in no_magic_attrs:
        handle_method(instance, method, reserved_args, arg_env)
    return instance


def _check_attr(attr: str, total_attrs: list, strict=True):
    for curr_attr in total_attrs:
        if strict and attr == curr_attr:
            return True
        elif not strict and attr in curr_attr:
            return True
    return False
