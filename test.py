i = 5


def func():
    global i
    i = 6


func()
print(i)
