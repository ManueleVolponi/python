from abc import abstractmethod, ABC

class Personaggio(ABC):
    def __init__(self, nome):
        self.nome = nome

        @abstractmethod
        def attacca(self):
            pass

class Guerriro(Personaggio):
    def attacca(self):
        return f"{self.nome} attacca con la spada"
    
class Mago(Personaggio):
    def attacca(self):
        return f"{self.nome} attacca con la magia"
    
class Ladro(Personaggio):
    def attacca(self):
        return f"{self.nome} attacca con il pugnale"

if __name__ == '__main__':
    g = Guerriro('Conan')
    m = Mago('Gandalf')
    l = Ladro('Bilbo')

    print(g.attacca())
    print(m.attacca())
    print(l.attacca())

    # p = Personaggio('Pippo') # Errore