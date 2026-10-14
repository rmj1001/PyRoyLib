from typing import TypeVar, Callable

T = TypeVar("T")
U = TypeVar("U")


class InputException(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(msg)


def prompt[T](msg: str = "input > ",
              default: T | None = None,
              blank: bool = False,
              tries: int = 1,
              strip: bool | str | None = None,
              pre_val_func: Callable | None = None,
              val_func: Callable[[T], bool] | None = None,
              post_val_func: Callable | None = None) -> T:
    """Prompt user for input, add colon after prompt message"""
    output = ""

    for i in range(tries):
        output = input(f"{msg}: ")

        if not blank and output == "":
            continue

    if not blank and output == "":
        if default is not None:
            return default
        else:
            raise InputException("Prompt does not allow blank input and user exceeded allowed tries.")

    if isinstance(strip, bool) and strip:
        output = output.strip()

    if isinstance(strip, str):
        output = output.strip(strip)

    if pre_val_func is not None:
        output = pre_val_func(output)

    if val_func is not None:
        is_val: bool = val_func(output)

        if not is_val and default is not None:
            return default

        if not is_val and default is None:
            raise InputException("User input is invalid and default value was not provided.")

    if post_val_func is not None:
        output = post_val_func(output)

    return output


def input_bool(msg: str="bool > ",
               default: bool | None = None,
               blank: bool = False,
               tries: int = 1,
               strip: bool | str | None = None,
               pre_val_func: Callable | None = None,
               val_func: Callable[[U], bool] | None = None,
               post_val_func: Callable | None = None) -> bool:
    """Get a boolean from user input"""
    return prompt(msg, default, blank, tries, strip, pre_val_func, val_func, post_val_func)


def input_str(msg: str="str > ",
              default: str | None = None,
              blank: bool = False,
              tries: int = 1,
              strip: bool | str | None = None,
              pre_val_func: Callable | None = None,
              val_func: Callable[[U], bool] | None = None,
              post_val_func: Callable | None = None) -> str:
    """Get a string from user input"""
    return prompt(msg, default, blank, tries, strip, pre_val_func, val_func, post_val_func)


def input_int(msg: str="int > ",
              default: int | None = None,
              blank: bool = False,
              tries: int = 1,
              strip: bool | str | None = None,
              pre_val_func: Callable | None = None,
              val_func: Callable[[U], bool] | None = None,
              post_val_func: Callable | None = None,
              minimum: int | None = None,
              maximum: int | None = None) -> int:
    """Get an integer from user input"""
    output: int = prompt(msg, default, blank, tries, strip, pre_val_func, val_func, post_val_func)

    if minimum is not None and output < minimum:
        return minimum

    if maximum is not None and output > maximum:
        return maximum

    return output


def input_float(msg: str = "float > ",
                default: float | None = None,
                blank: bool = False,
                tries: int = 1,
                strip: bool | str | None = None,
                pre_val_func: Callable | None = None,
                val_func: Callable[[U], bool] | None = None,
                post_val_func: Callable | None = None,
                minimum: float | None = None,
                maximum: float | None = None) -> float:
    """Get a float from user input"""
    output: float = prompt(msg, default, blank, tries, strip, pre_val_func, val_func, post_val_func)

    if minimum is not None and output < minimum:
        return minimum

    if maximum is not None and output > maximum:
        return maximum

    return output


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
