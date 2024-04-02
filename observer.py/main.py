from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def aggiorna(self, status: bool):
        pass

class Subject(ABC):
    def __init__(self):
        self._status = False
        self._observers = []

    def notifica(self, status: bool):
        for observer in self._observers:
            observer.aggiorna(status)

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

class SistemaDiAllarme(Subject):
    def __init__(self):
        super().__init__()
        self._status = False


    def attiva(self):
        self._status = True
        self.notifica(self._status)

    def disattiva(self):
        self._status = False
        self.notifica(self._status)

class PonteDiComando:
    def aggiorna(self, status: bool):
        if status == True:
            print("Ponte di comando: Allarme attivato")
        else:
            print("Ponte di comando: Allarme disattivato")

class StazioneSpaziale:
    def aggiorna(self, status: bool):
        if status == True:
            print("Stazione spaziale: Allarme attivato")
        else:
            print("Stazione spaziale: Allarme disattivato")

if __name__ == "__main__":
    sistema_di_allarme = SistemaDiAllarme()
    ponte_di_comando = PonteDiComando()
    stazione_spaziale = StazioneSpaziale()

    sistema_di_allarme.attach(ponte_di_comando)
    sistema_di_allarme.attach(stazione_spaziale)

    print("\nInizio primo allarme:")
    sistema_di_allarme.attiva()
    print("\nFine primo allarme:")
    sistema_di_allarme.disattiva()

    sistema_di_allarme.detach(ponte_di_comando)

    print("\nNuovo allarme senza il ponte di comando:")
    sistema_di_allarme.attiva()
    sistema_di_allarme.disattiva()
