# SPDX-FileCopyrightText: 2023-present Gabriel Chaperon <gabrielchaperonb@gmail.com>
#
# SPDX-License-Identifier: MIT
import functools

from autocast import _typing as tp

__all__ = ["coerces", "becomes"]

sentinel = object()
T = tp.TypeVar("T")
P = tp.ParamSpec("P")

becomes = tp.Annotated[T, sentinel]

annotated_type_names = {"AnnotatedMeta", "_AnnotatedAlias"}


def should_convert(hint: tp.Any) -> bool:
    return type(hint).__name__ in annotated_type_names and sentinel in hint.__metadata__


def coerces(fun: tp.Callable[P, T]) -> tp.Callable[P, T]:
    type_hints = tp.get_type_hints(fun, include_extras=True)

    @functools.wraps(fun)
    def inner(*args: P.args, **kwargs: P.kwargs) -> T:
        return fun(
            *(
                hint.__origin__(arg) if should_convert(hint) else arg
                for arg, hint in zip(args, type_hints.values())
            ),
            **{
                k: hint.__origin__(arg) if should_convert(hint) else arg
                for k, hint, arg in zip(
                    kwargs.keys(),
                    map(type_hints.__getitem__, kwargs.keys()),
                    kwargs.values(),
                )
            },
        )

    return inner
