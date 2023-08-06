# Welcome to BonkersDB

### An easy-to-use key-value database

------

## How to Use:
Import BonkersDB:
```python
from BonkersDB import BonkersDB
# Import BonkersDB
```
Now you can start using it. Let's create a value.
```python
database = BonkersDB("./database.db") 
# create a database
database.set("name" , "Josh")
# set an item
```
Now let's pull a value:
```python
name = database.get("name")
# pull an item from the database
print(name)
# print it
```
You're all set! Enjoy BonkersDB! 🎉