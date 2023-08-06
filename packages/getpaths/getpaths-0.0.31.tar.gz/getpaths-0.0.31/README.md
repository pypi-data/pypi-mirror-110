# getpath
Helps with pathing in python scripts. Inspired by pathlib.

# IMPORTING
```
from getpaths import getpath
```

# USING CURRENT FILE PATH
```
current_dir = getpath() # current file's path
```

# USER-SPECIFIED PATH
```
custom_dir = getpath('a','b',custom=True)
print(custom_dir)
# /a/b
```

# ADD FILES
```
custom_dir/'example.txt'
# /a/b/example.txt

custom_dir.add('/a/example.txt')
# /a/b/example.txt
```

#  GO UP THE DIRECTORY
```
custom_dir = getpath('a','b',custom=True)

custom_dir/'..'
# /a

custom_dir.add('..')
# /a

custom_dir.up(1)
# /a
```

# LIST EXISTING FILES AND FOLDERS
```
custom_dir.ls()
# /a/b/example.txt
# throws error if path does not exist
```