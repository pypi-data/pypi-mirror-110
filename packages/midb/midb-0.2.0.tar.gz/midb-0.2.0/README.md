# Mostly Invisible Database

A database access layer that acts like python in-memory objects. 

---
Disclaimer: Only minimal attempts have been made at speed. And mainly
intended for personal projects. Deeply nested data structures will 
likely be slow.

---
Example:

``` python
>>> import midb
>>> root = midb.get_root('db_file.db')
>>> root['test'] = 1
>>> root['test2'] = {'test3': 3}
>>> exit()
```
later ...
``` python
>>> import midb
>>> root = midb.get_root('db_file.db')
>>> root['test']
1
>>> root['test2']['test3']
3
>>> root['test2']
PDict({'test3': 3}, _backend=SQLiteBackend(filename="db_file.db"), _id=1, _temp=None)
>>> root['test2'].in_memory()
{'test3': 3}
>>> exit()
```

---
### What's currently supported?
Currently, the types that are supported are:
* str
* None
* bool
* int
* float
* datetime.datetime
* datetime.date
* datetime.time
* dict (silently converted to PDict, must not contain unsupported types)
* tuple (silently convert to PTuple, must not contain unspported types, currently can't be used as PDict keys.)

---
### Up Next:
* Support for lists.

---
### Future:

* Support for hashable tuples as dict keys.
* Support for custom objects.

---
### Bugs

Please report bugs at https://gitlab.com/gossrock/midb/-/issues 






