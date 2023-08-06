# PythonReact

Did you ever think: "We need a JS library turned into a python module used for console output in stead of rendering a webpage."? No? Well I did. So here it is.

## Installation

This package is on [pypi](https://pypi.org/project/pythonreact/).  
Installing can be done via ``pip``

Windows:

```ps
pip install pythonreact
```

Mac/ Linux:

```sh
pip3 install pythonreact
```

## Usage

If you are familliar with the JS library react this should be very easy.

### Component

Everything is a component.  
To create a new component, make a class that inherits from ``PythonReact.Component``

```py
import PythonReact


class MyComponent(PythonReact.Component):
    pass

```

### Hello python react

To show something in the console we will add a render function. This render function should return a list of printable items or other Components.

```py
import PythonReact


class MyComponent(PythonReact.Component):
    def render(self) -> list:
        return [
            "Hello",
            "Python React"
        ]

```

Let's make an object of that type:

```py
# snip
my_comp = MyComponent()
```

It will automatically start printing now.
And it will render your function.

### State

If you have used React you know about state.

To create a state add it to the ``__init__`` of your component.
And then simply call the variables in your render function.

```py
import PythonReact


class MyComponent(PythonReact.Component):
    def __init__(self):
        self.state = {
            "name": "Donkere",
        }

        super().__init__()

    def render(self) -> list:
        return [
            f"Hello {self.state['name']}!",
        ]


my_comp = MyComponent()

>>>
Hello Donkere!

```

#### Set state

Just as in React there is a set state function.

```py
import PythonReact


class MyComponent(PythonReact.Component):
    def __init__(self):
        self.state = {
            "name": "Donkere",
        }

        super().__init__()

    def render(self) -> list:
        return [
            f"Hello {self.state['name']}!",
        ]


my_comp = MyComponent()
my_comp.set_state({"name": "New Name"})

>>>
Hello Donkere!
# Screen get's cleared
Hello New Name!

```
