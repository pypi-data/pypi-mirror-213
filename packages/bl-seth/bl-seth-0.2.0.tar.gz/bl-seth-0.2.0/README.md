# Seth

A setting management library. By grouping all your application settings in one class,
it's easier to document.

First, define a class for your settings. It must be a `dataclass` (or even better,
a frozen `dataclass`) and inherit from `seth.Settings`.

```python
from dataclasses import dataclass
from typing import Optional

from bl_seth import Settings

@dataclass
class MySettings(Settings):
    MANDATORY: str
    "A mandatory string."
    
    DEFAULT: str = "default"
    """A string that defaults to '"default"'."""

    INTEGER: int = 1
    "An integer that defaults to '1'."

    OPTIONAL: Optional[str] = None
    "An optional value."
```

Then instantiate it using its `from_dict` class method. Most probably, the dictionary
is built from the environment.

```python
import os

settings = MySettings.from_dict(os.environ)
```

You can now directly access its attributes.

```python
settings.DEFAULT == "default"
settings.OPTIONAL is None
```
