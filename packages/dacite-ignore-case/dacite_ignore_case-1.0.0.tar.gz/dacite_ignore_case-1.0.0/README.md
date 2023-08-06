# dacite-ignore-case
Initialize dataclasses from dictionaries (based on dacite) but with case ignorance.

## Usage
```python
import dacite_ignore_case
from dataclasses import dataclass


@dataclass
class MyClass:
  myKey: str
  
  
data = {'mykey': 'value'}

c = dacite_ignore_case.from_dict(MyClass, data)
```

## Installation
`pip3 install dacite_ignore_case`
