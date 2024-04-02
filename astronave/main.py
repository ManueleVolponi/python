import math

class Astronave:
    def __init__(self, x: int ,y: int):
        self.__x__ = x
        self.__y__ = y

    def sposta(self, x, y):
        self.__x__ += x
        self.__y__ += y
        return self.__x__, self.__y__

    def distanza_da(self, x, y):
        return math.sqrt((self.__x__ - x)**2 + (self.__y__ - y)**2)

astro = Astronave(0, 0)
print(astro.sposta(5, 5))
print(astro.distanza_da(0, 0))
