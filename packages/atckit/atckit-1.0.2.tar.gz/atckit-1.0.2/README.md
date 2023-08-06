# ATCKit

AccidentallyTheCable's Utility Kit

- [ATCKit](#atckit)
  - [About](#about)
    - [How does it work?](#how-does-it-work)
  - [Usage](#usage)
    - [FunctionSubscriber](#functionsubscriber)
  - [UtilFuncs](#utilfuncs)

## About

This is a small kit of classes, util functions, etc that I found myself rewriting or reusing frequently, and instead of copying everywhere, they are now here.


### How does it work?

Do the needfuls.... *do the needful dance*

Literally, import whatever you need to use..

## Usage

### FunctionSubscriber

A Class container for Function callback subscription via `+=` or `-=`. Functions can be retrieved in order of addition.

```
subscriber = FunctionSubscriber()

def a():
    print("I am a teapot")

def b():
    print("I am definitely totally not also a teapot, I swear")

subscriber += a
subscriber += b

for cb in subscriber.functions:
    cb()

>> I am a teapot
>> I am definitely totally not also a teapot, I swear
```

This class uses the `typing.Callable` type for function storage. You can extend the `FunctionSubscriber` class to define the
callback function parameters, etc.

```
class MySubscriber(FunctionSubscriber):
    """My Function Subscriber
    Callback: (bool) -> None
    """

    _functions:list[Callable[[bool],None]]

    def __iadd__(self,fn:Callable[[bool],None]) -> Self:
        """Inline Add. Subscribe Function
        @param method \c fn Method to Subscribe
        """
        return super().__iadd__(fn)

    def __isub__(self,fn:Callable[[bool],None]) -> Self:
        """Inline Subtract. Unsubscribe Function
        @param method \c fn Method to Unsubscribe
        """
        return super().__isub__(fn)
```

## UtilFuncs

A Class containing various static methods:

 - scan_dir: Search a specified Path, and execute a callback function on discovered files.
   - Allows exclusion of Files/Dirs via regex pattern matching
 - deep_sort: Sort a Dictionary recursively, including through lists of dicts
 - check_pid: Check if a process ID exists (via kill 0)
 - register_signals: Register Shutdown / Restart Handlers
   - Check for Shutdown via UtilFuncs.shutdown (bool)
   - Check for Restart via UtilFuncs.restart (bool)
