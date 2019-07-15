
def outer(func):
    def inner(*args,**kwargs):
        print('Before func')
        # func()
        print('After func')
        return func(*args,**kwargs)

    return inner

@outer
def test():
    return 'this is a test'

print(test())