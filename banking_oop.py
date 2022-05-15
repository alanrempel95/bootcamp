import json


def write_to_file(data):
    with open('bank_records.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def read_from_file():
    with open('bank_records.json', 'r', encoding='utf-8') as f:
        json.load(f)


class BalanceError(Exception):
    pass


class Customer:
    def __init__(self, first_name, last_name, address, identifier):
        self.first_name = first_name
        self.last_name = last_name
        self.name = first_name + " " + last_name
        self.address = address
        self.identifier = identifier

    def __eq__(self, other):
        return (self.identifier == other.identifier) and (self.name == other.name)

    def __str__(self):
        cust_str = """
        Customer:
            name: {name}
            balance: {balance}
        """.format(name=self.name, balance=self.balance)
        return cust_str

    def __repr__(self):
        return "Customer('{name}', {balance})".format(name=self.name, balance=self.balance)


class BankAccount:
    def __init__(self, balance=0):
        if balance < 0:
            raise BalanceError("Balance must be non-negative!")
        else:
            self.balance = balance

    def withdraw(self, amount):
        if self.balance - amount < 0:
            raise BalanceError("Transaction would cause customer to be overdrawn!")
        else:
            self.balance -= amount
        return self.balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance


class SavingsAccount(BankAccount):
    def __init__(self, balance, interest_rate):
        BankAccount.__init__(self, balance)
        self.interest_rate = interest_rate

    def compute_interest(self, n_periods=1):
        return self.balance * ((1 + self.interest_rate) ** n_periods - 1)


class CheckingAccount(BankAccount):
    def __init__(self, balance, limit):
        BankAccount.__init__(self, balance)
        self.limit = limit

    def withdraw(self, amount, fee=0):  # review logic
        if amount <= self.limit:
            BankAccount.withdraw(self, amount + fee)
        else:
            BankAccount.withdraw(self, self.limit + fee)


class Employee(Customer):
    MIN_SALARY = 70000

    def __init__(self, first_name, last_name, address, identifier, salary=MIN_SALARY):
        Customer.__init__(self, first_name, last_name, address, identifier)
        self.salary = max(salary, Employee.MIN_SALARY)

    def give_raise(self, raise_amount):
        self.salary += raise_amount

    def monthly_salary(self):
        return self.salary / 12.0
