# decorlib

Python library with decorators for ease of development

## Usage

```python
from decorlib import *

@performance
def my_function():
    pass

@retry(5, delay=3.0)
def my_functions():
    pass
```