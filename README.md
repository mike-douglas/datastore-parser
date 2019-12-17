# Datastore Parser

This package parses Lua files that are generated through the World of Warcraft addon Altoholic. It uses a Lua AST to produce Python dicts for use in python apps.

## Example use

```python
from datastore_parser import lua_to_dict

with open('foo.lua') as lua:
  data = lua_to_dict(lua.read())

  print(data)
```
