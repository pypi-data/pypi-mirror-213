from __future__ import annotations

import copyreg
import sys
import warnings
from abc import ABC
from copy import deepcopy
from itertools import chain, combinations
from typing import Callable, List, Optional, Tuple, Union

import numpy as np
import scipy as sp
from numpy.random import randint
from py_expression_eval import Parser

__authors__ = ["Hao Wang"]


def identity(x):
    return x


def bilog(x):
    return np.sign(x) * np.log(1 + np.abs(x))


def logit_inv(x):
    return 1 / (1 + np.exp(-x))


def bilog_inv(x):
    return np.sign(x) * (np.exp(np.abs(x)) - 1)


def log10_inv(x):
    return np.power(10, x)


MAX = sys.float_info.max
TRANS = {
    "linear": [identity, [-MAX, MAX]],
    "log": [np.log, [1e-300, MAX]],
    "log10": [np.log10, [1e-300, MAX]],
    "logit": [sp.special.logit, [1e-300, 1]],
    "bilog": [bilog, [-MAX, MAX]],
}
INV_TRANS = {
    "linear": identity,
    "log": np.exp,
    "log10": log10_inv,
    "logit": logit_inv,
    "bilog": bilog_inv,
}


def _gen_action(v):
    def _action(_):
        return v

    return _action


def _gen_map_func(bounds, step=0):
    def _map_func(i):
        if hasattr(bounds, "__iter__"):
            return bounds[i]
        else:
            return bounds + i * step

    return _map_func


class Variable(ABC):
    """Base class for decision variables"""

    def __init__(
        self,
        bounds: List[int, float, str],
        name: str,
        default_value: Union[int, float, str] = None,
        conditions: str = None,
        action: Union[callable, int, float, str] = 0,
    ):
        """Base class for decision variables

        Parameters
        ----------
        bounds : List[int, float, str]
            a list/tuple giving the range of the variable.
                * For `Real`, `Integer`: (lower, upper)
                * For `Ordinal` and `Discrete`: (value1, value2, ...)
        name : str
            variable name
        default_value : Union[int, float, str], optional
            default value, by default None
        conditions : str, optional
            a string specifying the condition on which the variable is problematic, e.g.,
            being either invalid or ineffective, by default None. The variable name in
            this string should be quoted as `var name`. Also, you could use multiple
            variables and logic conjunctions/disjunctions therein.
            Example: "`var1` == True and `var2` == 2"
        action : Union[callable, int, float, str], optional
            the action to take when `condition` evaluates to True, by default `lambda x: x`.
            It can be simply a fixed value to which the variable will be set, or a callable
            that determines which value to take.
        """
        if len(bounds) > 0 and isinstance(bounds[0], list):
            bounds = bounds[0]
        self.name: str = name
        self.bounds = tuple(bounds)
        self.set_default_value(default_value)
        self.set_conditions(conditions, action)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        msg = f"{self.name} -> {type(self).__name__} | range: {self.bounds}"
        if self.default_value is not None:
            msg += f" | default: {self.default_value}"
        return msg

    def __contains__(self, _: Union[float, str, object]) -> bool:
        pass

    def __eq__(self, var: Variable) -> bool:
        return (
            self.__class__ == type(var)
            and self.bounds == var.bounds
            and self.default_value == var.default_value
            and self.name == var.name
            # and self.conditions["string"] == var.conditions["string"]
            # and self.action == var.action
        )

    def __ne__(self, var: Variable) -> bool:
        return not self.__eq__(var)

    def copyfrom(self, var: Variable):
        """copy from another variable of the same type"""
        if not isinstance(var, type(self)):
            raise TypeError(f"copying from variable {var} which has a type different type than {type(self)}")
        self.__dict__.update(**deepcopy(var.__dict__))

    def set_default_value(self, value):
        """validate the default value first"""
        if value is not None:
            assert self.__contains__(value)
        self.default_value = value

    def set_conditions(self, conditions: str, action: Union[callable, int, float, str] = 0):
        self.conditions = None
        if conditions is not None:
            # TODO: add parsing exceptions here
            expr = Parser().parse(conditions)
            self.conditions = {"string": conditions, "expr": expr, "vars": expr.variables()}

        self.action = None
        # if isinstance(action, (int, float, str)):
        #     self.action = _gen_action(action)
        # elif hasattr(action, "__call__"):
        #     self.action = action


class Real(Variable):
    """Real-valued variable taking its value in a continuum"""

    def __init__(
        self,
        bounds: Tuple[float, float],
        name: str = "r",
        default_value: float = None,
        precision: int = None,
        scale: str = "linear",
        **kwargs,
    ):
        """Real-valued variable taking its value in a continuum

        Parameters
        ----------
        bounds : [Tuple[float, float]
            the lower and upper bound
        name : str, optional
            the variable name, by default 'r'
        default_value : float, optional
            the default value, by default None
        precision : int, optional
            the number of digits after decimal, by default None
        scale : str, optional
            the scale on which uniform sampling is performed, by default 'linear'
        """
        assert bounds[0] < bounds[1]
        assert scale in TRANS.keys()
        assert precision is None or isinstance(precision, int)
        super().__init__(bounds, name, default_value, **kwargs)
        self.precision: int = precision
        self.scale = scale

    def __hash__(self):
        return hash((self.name, self.bounds, self.default_value, self.precision, self.scale))

    def __str__(self):
        msg = super().__str__()
        if self.precision:
            msg += f" | precision: .{self.precision}f"
        msg += f" | scale: {self.scale}"
        return msg

    def __contains__(self, x: Union[float, str]) -> bool:
        return self.bounds[0] <= x <= self.bounds[1]

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        if scale is None:
            scale = "linear"

        assert scale in TRANS.keys()
        self._scale: str = scale
        self._trans: Callable = TRANS[scale][0]
        self._inv_trans: Callable = INV_TRANS[scale]
        _range = TRANS[scale][1]
        bounds = list(self.bounds)

        if (bounds[0] < _range[0]) or (bounds[0] > _range[1]):
            bounds[0] = _range[0]
            warnings.warn(
                f"lower bound {bounds[0]} not in the working "
                f"range of the given scale {self._scale} is set to the default value {_range[0]}"
            )

        if (bounds[1] < _range[0]) or (bounds[1] > _range[1]):
            bounds[1] = _range[1]
            warnings.warn(
                f"upper bound {bounds[1]} not in the working "
                f"range of the given scale {self._scale} is set to the default value {_range[1]}"
            )
            # raise ValueError(
            #     f"upper bound {self.bounds[1]} is invalid for the given scale {self._scale}"
            # )
        self.bounds = tuple(bounds)
        self._bounds_transformed = self._trans(self.bounds)

    def to_linear_scale(self, X):
        return X if self.scale == "linear" else self._inv_trans(X)

    def round(self, X):
        """Round the real-valued components of `X` to the
        corresponding numerical precision, if given
        """
        X = deepcopy(X)
        if self.precision is not None:
            X = np.clip(np.round(X, self.precision), self.bounds[0], self.bounds[1])
        return X


class _Discrete(Variable):
    """Represents Integer, Ordinal, Bool, and Discrete"""

    def __init__(self, bounds, *args, **kwargs):
        # get rid of duplicated levels
        bounds = list(dict.fromkeys(bounds))
        # map discrete values (bounds) to integers for sampling
        self._map_func: callable = None
        self._size: int = None
        super().__init__(bounds, *args, **kwargs)

    def __contains__(self, x: Union[int, str]) -> bool:
        return x in self.bounds

    def __hash__(self):
        return hash((self.name, self.bounds, self.default_value))

    def sample(self, N: int = 1, **_) -> List:
        return list(map(self._map_func, randint(0, self._size, N)))


class Discrete(_Discrete):
    """Discrete variable, whose values should come with a linear order"""

    def __init__(self, bounds, name: str = "d", default_value: Union[int, str] = None, **kwargs):
        super().__init__(bounds, name, default_value, **kwargs)
        self._map_func = _gen_map_func(self.bounds)
        self._size = len(self.bounds)


class Subset(Discrete):
    """A discrete variable created by enumerating all subsets of the input `bounds`"""

    def __init__(self, bounds, name: str = "s", default_value: Union[int, str] = None, **kwargs):
        self._bounds = bounds
        bounds = list(chain.from_iterable(map(lambda r: combinations(bounds, r), range(1, len(bounds) + 1))))
        super().__init__(bounds, name, default_value, **kwargs)

    def __str__(self):
        msg = f"{self.name} -> {type(self).__name__} | range: 2 ^ {self._bounds}"
        if self.default_value is not None:
            msg += f" | default: {self.default_value}"
        return msg


class Ordinal(_Discrete):
    """A generic ordinal variable, whose values should come with a linear order"""

    def __init__(self, bounds, name: str = "ordinal", default_value: int = None, **kwargs):
        super().__init__(bounds, name, default_value, **kwargs)
        self._map_func = _gen_map_func(self.bounds)
        self._size = len(self.bounds)


class Integer(_Discrete):
    """Integer variable"""

    def __init__(
        self,
        bounds: Tuple[int],
        name: str = "i",
        default_value: int = None,
        step: Optional[Union[int, float]] = 1,
        **kwargs,
    ):
        super().__init__(bounds, name, default_value, **kwargs)
        assert len(self.bounds) == 2
        assert self.bounds[0] < self.bounds[1]
        assert all(map(lambda x: isinstance(x, (int, float)), self.bounds))
        self.step = step
        self._map_func = _gen_map_func(self.bounds[0], self.step)
        self._size = int(np.floor((self.bounds[1] - self.bounds[0]) / self.step) + 1)

    def __contains__(self, x: int) -> bool:
        return self.bounds[0] <= x <= self.bounds[1]

    def __hash__(self):
        return hash((self.name, self.bounds, self.default_value, self.step))

    def __str__(self):
        msg = super().__str__()
        msg += f" | step: {self.step}"
        return msg


class Bool(_Discrete):
    """Boolean variable"""

    def __init__(self, name: str = "bool", default_value: int = True, **kwargs):
        # NOTE: remove `bounds` if it presents in the input
        kwargs.pop("bounds", None)
        assert default_value is None or isinstance(default_value, bool)
        super().__init__((False, True), name, default_value, **kwargs)
        self._map_func = bool
        self._size = 2
