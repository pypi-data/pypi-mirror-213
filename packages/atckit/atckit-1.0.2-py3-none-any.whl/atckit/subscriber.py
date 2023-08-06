import logging

from typing import Callable
import typing_extensions

class FunctionSubscriber:
    """ Function subscriber


    Provides a += / -= interface for adding callback functions

    Example:

    \li Define some functions

        \code{.py}
        def a():
            print("a")
        def b():
            print("b")
        \endcode

    \li Create a subscriber and Subscribe the above functions
        \code{.py}
        f = FunctionSubscriber()
        f += a
        f += b
        print(f.functions)
        \endcode

    \li Remove a subscription
        \code{.py}
        f -= a
        print(f.functions)
        \endcode

    \li Execute subscribed functions
        \code{.py}
        for method_def in f.functions:
            method_def()
        \endcode
    """

    _functions:list[Callable]

    @property
    def functions(self) -> list[Callable]:
        """\b \e PROPERTY; Currently Subscribed Functions"""
        return self._functions

    def __init__(self) -> None:
        """Initializer
        """
        self._functions = []

    def __iadd__(self,fn:Callable) -> typing_extensions.Self:
        """Inline Add. Subscribe Function
        @param method \c fn Method to Subscribe
        """
        if fn not in self._functions:
            logging.debug(f"Adding Function {fn.__qualname__}")
            self._functions.append(fn)
        return self

    def __isub__(self,fn:Callable) -> typing_extensions.Self:
        """Inline Subtract. Unsubscribe Function
        @param method \c fn Method to Unsubscribe
        """
        if fn not in self._functions:
            return self
        i:int = self._functions.index(fn)
        self._functions.pop(i)
        logging.debug(f"Removing Function {fn.__qualname__}")
        return self
