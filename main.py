from src.container import Container
from src.interfaces import IContext

container = Container()


class IDepend:
    pass


@container.component(interface=IDepend)
class Depend1(IDepend):
    def __init__(self):
        pass


@container.component()
class Depend2(IDepend):
    def __init__(self):
        pass


@container.component()
class User(IContext):

    @container.autowired
    def __init__(self, depend1: IDepend, depend2: Depend2):
        self.depend1 = depend1
        self.depend2 = depend2

    def say_hello(self):
        print('hello')

    def __repr__(self):
        return f'{self.depend1}, {self.depend2}'

    def on_enter(self):
        print('user enter')

    def on_exit(self):
        print('user exit')


@container.autowired
def main(user: User):
    user.say_hello()


if __name__ == '__main__':
    main()
