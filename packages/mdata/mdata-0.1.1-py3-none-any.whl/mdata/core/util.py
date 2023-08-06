from __future__ import annotations

from collections.abc import Iterable, Collection


def intersection(a, b) -> set:
    if a is None or b is None:
        return set()
    else:
        return set(a) & set(b)


def symmetric_difference(a, b) -> tuple[set, set]:
    if a is None and b is None:
        return set(), set()
    elif a is None:
        return set(), set(b)
    elif b is None:
        return set(a), set()
    else:
        a, b = set(a), set(b)
        return a - b, b - a


def mangle_arg_to(arg: None | str | Iterable, cls, rm_duplicates=False, preserve_order=True, preserve_none=False):
    if arg is None:
        return arg if preserve_none else cls()
    elif not type(arg) is str and isinstance(arg, Iterable):
        if rm_duplicates:
            if not preserve_order:
                return cls(set(arg))
            elif preserve_order:
                s = set()
                return cls(
                    (i for i in arg if (i not in s) and (s := s | {i})))  # the things I do for an (almost) one-liner
        else:
            return cls(arg)
    else:
        return cls((arg,))


def mangle_arg_to_set(arg, **kwargs):
    return mangle_arg_to(arg, set, **kwargs)


def mangle_arg_to_list(arg, rm_duplicates=True, preserve_order=True, **kwargs):
    return mangle_arg_to(arg, list, rm_duplicates=rm_duplicates, preserve_order=preserve_order, **kwargs)


def mangle_arg_to_tuple(arg, rm_duplicates=True, preserve_order=True, **kwargs):
    return mangle_arg_to(arg, tuple, rm_duplicates=rm_duplicates, preserve_order=preserve_order, **kwargs)


def assert_in(items: Iterable, allowed: Collection):
    assert all(i in allowed for i in items)


def mangle_arg_with_bool_fallback(mangler, arg, if_true=None, if_false=None, treat_none_as_false=True, **kwargs):
    if arg is None and treat_none_as_false:
        arg = if_false
    elif isinstance(arg, bool):
        arg = if_true if arg else if_false
    return mangler(arg, **kwargs)
