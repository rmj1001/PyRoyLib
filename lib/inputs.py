from typing import TypeVar, Callable
from monads import Option, some, nada

T = TypeVar("T")
U = TypeVar("U")


class InputException(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(msg)


def prompt[T](msg: str = "input > ",
              default: Option[T] = nada(),
              blank: bool = False,
              tries: int = 1,
              strip: Option[bool|str] = nada(),
              pre_val_func: Option[Callable] = nada(),
              val_func: Option[Callable[[T], bool]] = nada(),
              post_val_func: Option[Callable] = nada()) -> Option[T]:
    """Prompt user for input, add colon after prompt message"""
    output: Option[T] = nada()

    for i in range(tries):
        output = some(input(f"{msg}: "))

        if not blank and output == "":
            continue

    if not blank and output == "":
        output = default

    strip = strip.unwrap_or(False)

    if isinstance(strip, str):
        output = output.flatmap(lambda s: s.strip(strip))

    if isinstance(strip, bool) and strip:
        output = output.flatmap(lambda s: s.strip())

    # Run a function on the input before validation if one is passed
    if pre_val_func.is_some():
        func = pre_val_func.unwrap()
        output = output.flatmap(func)

    # Try to validate input. If validation function returns False, set output to default
    if val_func.is_some():
        func = val_func.unwrap()

        if output.flatmap(func) == some(False):
            output = default

    # Run a function on the input after validation if one is passed
    if post_val_func.is_some():
        func = post_val_func.unwrap()
        output = output.flatmap(func)

    return output


def input_bool(msg: str = "bool > ",
              default: Option[bool] = nada(),
              blank: bool = False,
              tries: int = 1,
              strip: Option[bool|str] = nada(),
              pre_val_func: Option[Callable] = nada(),
              val_func: Option[Callable[[T], bool]] = nada(),
              post_val_func: Option[Callable] = nada()) -> Option[bool]:
    """Get a boolean from user input"""
    return prompt(msg, default, blank, tries, strip, pre_val_func, val_func, post_val_func)


def input_str(msg: str = "str > ",
              default: Option[str] = nada(),
              blank: bool = False,
              tries: int = 1,
              strip: Option[bool|str] = nada(),
              pre_val_func: Option[Callable] = nada(),
              val_func: Option[Callable[[T], bool]] = nada(),
              post_val_func: Option[Callable] = nada()) -> Option[str]:
    """Get a string from user input"""
    return prompt(msg, default, blank, tries, strip, pre_val_func, val_func, post_val_func)


def input_int(msg: str = "int > ",
              default: Option[int] = nada(),
              blank: bool = False,
              tries: int = 1,
              strip: Option[bool|str] = nada(),
              pre_val_func: Option[Callable] = nada(),
              val_func: Option[Callable[[T], bool]] = nada(),
              post_val_func: Option[Callable] = nada(),
              minimum: Option[int] = nada(),
              maximum: Option[int] = nada()) -> Option[int]:
    """Get an integer from user input"""
    output: Option[int] = prompt(msg, default, blank, tries, strip, pre_val_func, val_func, post_val_func)

    if output.is_nada():
        return output

    output_val = output.unwrap()

    if minimum.is_some():
        min_val = minimum.unwrap()

        return some(min(output_val, min_val))

    if maximum.is_some():
        max_val = maximum.unwrap()

        return some(max(output_val, max_val))

    return output


def input_float(msg: str = "float > ",
              default: Option[float] = nada(),
              blank: bool = False,
              tries: int = 1,
              strip: Option[bool|str] = nada(),
              pre_val_func: Option[Callable] = nada(),
              val_func: Option[Callable[[T], bool]] = nada(),
              post_val_func: Option[Callable] = nada(),
              minimum: Option[float] = nada(),
              maximum: Option[float] = nada()) -> Option[float]:
    """Get a float from user input"""
    output: Option[float] = prompt(msg, default, blank, tries, strip, pre_val_func, val_func, post_val_func)

    if output.is_nada():
        return output

    output_val = output.unwrap()

    if minimum.is_some():
        min_val = minimum.unwrap()

        return some(min(output_val, min_val))

    if maximum.is_some():
        max_val = maximum.unwrap()

        return some(max(output_val, max_val))

    return output


# TODO: Make this use Option
def input_yesno(msg: str = "yes/no > ",
                case_insensitive: bool = False,
                default: str | None = None,
                blank: bool = False,
                tries: int = 1,
                strip: bool | str | None = None,
                pre_val_func: Callable | None = None,
                val_func: Callable[[U], bool] | None = None,
                post_val_func: Callable | None = None) -> bool:
    """Return True if yes, False if no."""
    output: str = prompt(msg, default, blank, tries, strip, pre_val_func, val_func, post_val_func)
    yes: list[str] = ["yes", "y"]
    no: list[str] = ["no", "n"]

    if case_insensitive:
        output = output.lower()

    def valid(value: str) -> bool:
        return value in yes or value in no

    if valid(output):
        return output in yes

    if default is None:
        raise InputException("User input is invalid and default value was not provided.")

    if valid(default):
        return default in yes

    raise InputException("User input and default value are invalid.")


# TODO: Make this use Option
def input_choice(choices: list[T],
                 msg: str = "Choose an option below.\n",
                 case_insensitive: bool = False,
                 default: T | None = None,
                 blank: bool = False,
                 tries: int = 1,
                 strip: bool | str | None = None,
                 pre_val_func: Callable | None = None,
                 val_func: Callable[[U], bool] | None = None,
                 post_val_func: Callable | None = None) -> T:
    """Select value from list from user input"""
    for i in range(len(choices)):
        msg += f"- {choices[i]}\n"

    msg += "\n\nChoice > "

    output = prompt(msg, default, blank, tries, strip, pre_val_func, val_func, post_val_func)

    if case_insensitive:
        output = output.lower()
        choices = [choice.lower() for choice in choices]

    if output in choices:
        return output

    if default is None:
        raise InputException("User input is invalid and default value was not provided.")

    if default not in choices:
        raise InputException("User input and default value are invalid.")

    return default


# TODO: Make this use Option
def input_menu(choices: dict[U,T],
               msg: str = "Choose an option below.\n",
               case_insensitive: bool = False,
               default: T | None = None,
               blank: bool = False,
               tries: int = 1,
               strip: bool | str | None = None,
               pre_val_func: Callable | None = None,
               val_func: Callable[[U], bool] | None = None,
               post_val_func: Callable | None = None) -> T:
    """Select value from dictionary from user input"""
    for k, v in choices:
        msg += f"{k}. {v}\n"

    msg += "\n\nChoice > "

    output = prompt(msg, default, blank, tries, strip, pre_val_func, val_func, post_val_func)

    if case_insensitive:
        output = output.lower()
        new_choices = dict()

        for k, v in choices.items():
            new_choices[k.lower()] = v.lower()

        choices = new_choices

    if output in choices.keys():
        return choices[output]

    if output in choices.values():
        return output

    if default is None:
        raise InputException("User input is invalid and default value was not provided.")

    if default in choices.keys():
        return choices[default]

    if default in choices.values():
        return default

    raise InputException("User input and default value are invalid.")
