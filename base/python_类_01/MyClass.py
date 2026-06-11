class MyClass:
    """
    这是一个示例类，用于展示如何使用类
    """
    i = 123

    def test(self):
        print("hello world")


print(MyClass.i)
print(MyClass.test)

x = MyClass()
print(x.__dict__)

print(x.i)
print(x.test)
