class Computed:
    def __init__(self, r):
        self.r = r

    def area(self):
        return self.r * self.r * 3.14


c = Computed(5)
print(c.area())
