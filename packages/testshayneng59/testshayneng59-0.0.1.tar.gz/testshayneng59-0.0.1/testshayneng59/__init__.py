def my_hello(name=None):
    if name is None:
        return print('Hello World!')
    else:
        return print("Hello " + name)
my_hello(name='dung')
