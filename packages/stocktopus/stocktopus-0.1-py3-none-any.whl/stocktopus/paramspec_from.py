from typing import Callable, Concatenate, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")
S = TypeVar("S")
A = TypeVar("A")
B = TypeVar("B")


def paramspec_from(_: Callable[P, T]) -> Callable[[Callable[P, S]], Callable[P, S]]:
    def _fnc(fnc: Callable[P, S]) -> Callable[P, S]:
        return fnc

    return _fnc


def paramspec_from_drop1(_: Callable[Concatenate[A, P], T]) -> Callable[[Callable[P, S]], Callable[P, S]]:
    def _fnc(fnc: Callable[P, S]) -> Callable[P, S]:
        return fnc

    return _fnc


def paramspec_from_drop2(_: Callable[Concatenate[A, B, P], T]) -> Callable[[Callable[P, S]], Callable[P, S]]:
    def _fnc(fnc: Callable[P, S]) -> Callable[P, S]:
        return fnc

    return _fnc


def paramspec_from_add1(
    _: Callable[P, T], _1: type[A]
) -> Callable[[Callable[Concatenate[A, P], S]], Callable[Concatenate[A, P], S]]:
    def _fnc(fnc: Callable[Concatenate[A, P], S]) -> Callable[Concatenate[A, P], S]:
        return fnc

    return _fnc


def paramspec_from_add2(
    _: Callable[P, T], _1: type[A], _2: type[B]
) -> Callable[[Callable[Concatenate[A, B, P], S]], Callable[Concatenate[A, B, P], S]]:
    def _fnc(fnc: Callable[Concatenate[A, B, P], S]) -> Callable[Concatenate[A, B, P], S]:
        return fnc

    return _fnc
