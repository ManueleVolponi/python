class Account:
    def __init__(self, name, iban):
        self.name = name
        self.iban = iban
        

class BankAccount(Account):
    def __init__(self, name, balance, iban):
        super().__init__(name, iban)
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, amount):
        self.withdraw(self.__balance)
        self.deposit(amount)

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount > self.__balance:
            raise RuntimeError('Amount greater than available balance.')
        self.__balance -= amount

    def description(self):
        print("Name: ", self.name, "IBAN: ", self.iban, "Balance: ", self.__balance)


class BankAccountManager:
    @staticmethod
    def transfer(source, to, amount):
        source.withdraw(amount)
        to.deposit(amount)

c1 = BankAccount("John", 1000, "DE123456789")
c2 = BankAccount("Mary", 2000, "DE987654321")

BankAccountManager.transfer(c1, c2, 1500)


c1.description()
c2.description()