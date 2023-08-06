import functools
import inspect
import typing as tp
import re
import warnings

_REG_MODULE_NAME = r"^jijmodeling\..+"

class JijFutureWarning(FutureWarning):
    pass


def warning_message(
    old_name: str,
    new_name: tp.Optional[str] = None,
    *,
    kind: tp.Optional[tp.Literal["argument", "class", "function", "method", "property"]] = None
) -> str:
    _kind = "" if kind is None else kind + " "

    if new_name is None:
        message = (
            f"The {_kind}`{old_name}` is deprecated. "
            f"It will be removed when updating to jijmodeling 1.x.x."
        )
    else:
        message = (
            f"The {_kind}`{old_name}` is deprecated. "
            f"It will be changed when updating to jijmodeling 1.x.x. "
            f"Please use `{new_name}` instead."
        )

    return message


def warning_message_pos(func_name: str, max_len: int):
    return (
        f"`{func_name}` takes {max_len} positional arguments in jijmodeling 1.x.x. "
        "Please use keyword arguments for extra arguments." 
    )


def deprecated_name(
    old_name: str,
    new_name: tp.Optional[str] = None,
    kind: tp.Optional[tp.Literal["argument", "class", "function", "method", "property"]] = None
):
    def _deprecated_name(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            # Get where the function is called from.
            frame = inspect.stack()[1].frame
            module = inspect.getmodule(frame)
            if module is not None:
                # If the function is called from outside of jijmodeling.
                if re.match(_REG_MODULE_NAME, module.__name__) is None:
                    warnings.warn(
                        message=warning_message(old_name, new_name, kind=kind),
                        category=JijFutureWarning,
                        stacklevel=2, 
                    )
            return func(*args, **kwargs)
        return wrapped
    return _deprecated_name


def deprecated_kwargs(
    *,
    name: tp.Optional[str] = None,
    pos_len: tp.Optional[int] = None,
    changes: tp.Optional[tp.Dict[str, str]] = None,
    removes: tp.Optional[tp.List[str]] = None,
):
    if changes is None:
        changes = {}
    if removes is None:
        removes = []

    def _deprecated_kwargs(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            _kwargs = {key: value for key, value in kwargs.items() if value is not None}
            # Get where the function is called from.
            frame = inspect.stack()[1].frame
            module = inspect.getmodule(frame)
            if module is not None:
                # If the function is called from outside of jijmodeling.
                if re.match(_REG_MODULE_NAME, module.__name__) is None:
                    # `pos_len` is available only for method. Bacause of len(args) > pos_len+1.
                    if name is not None and pos_len is not None:
                        if len(args) > pos_len+1:
                            warnings.warn(
                                message=warning_message_pos(name, pos_len),
                                category=JijFutureWarning,
                                stacklevel=2,
                            )

                    # Warnings for keywrod that is removed in a future.
                    for removed_key in removes:
                        if removed_key in _kwargs.keys():
                            warnings.warn(
                                message=warning_message(removed_key, kind="argument"),
                                category=JijFutureWarning,
                                stacklevel=2,
                            )

                    # Warnings for keywrod that is changed in a future.
                    for old_key, new_key in changes.items():
                        if old_key in _kwargs.keys():
                            warnings.warn(
                                message=warning_message(old_key, new_key, kind="argument"),
                                category=JijFutureWarning,
                                stacklevel=2
                            )

            # Merge value of new keyword to value of old keyword.
            for old_key, new_key in changes.items():
                if new_key in _kwargs.keys():
                    _kwargs[old_key] = _kwargs.pop(new_key)

            return func(*args, **_kwargs)
        return wrapped
    return _deprecated_kwargs
