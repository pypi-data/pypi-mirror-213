# just a utility files for my codes


for using maths
```
x = sum(150,50)
```

For using tricolor

```
import turtle
from anim import anim
col = ("orange","white","green")

t = turtle.Turtle()

screen = turtle.Screen()
screen.bgcolor("black")
tricolor(color)
```
For checking Internet
```
if internet_available():
    print("Internet is active")
else:
    print("Internet disconnected")

```
for getting time
```
x = zonetime('Asia/Kolkata')
print(x)
```

For using tg functions 
```
from PyHarshit.tg import tgFunctions 

tgFunctions.copy_msg(arguments_here)
```
For using database
```python
>>> import PyHarshit.db as database
>>> db = database.load('test.db', False)

>>> db.set('key', 'value')

>>> db.get('key')
'value'

>>> db.dump()
True
```
