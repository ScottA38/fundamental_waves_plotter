#testing functionality of mapping class

from collections import Mapping

class Dog(Mapping):
    def __init__(self, age, breed):
        self.age = age
        self.breed = breed

    def __str__(self):
        return "I am a {}, BARK BARK!".format(self.breeds)

    def __iter__(self):
        return iter(self)

    def __len__(self):
        return len(self)

    def __getitem__(self, key):
        return self[key]

ter = Dog(3.5, "Alsatian")

ter.update({"yeh":[]})
