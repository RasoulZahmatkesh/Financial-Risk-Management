"""
capital_manager.py
"""
class CapitalManager:

    def __init__(self, initial_balance=0, reserve_percent=10):
        self.initial_balance = float(initial_balance)
        self.balance = float(initial_balance)
        self.reserve_percent = float(reserve_percent)

    def deposit(self, amount):
        amount = float(amount)
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        amount = float(amount)
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        return self.balance

    def reserve(self):
        return (self.balance * self.reserve_percent / 100)

    def tradable_balance(self):
        value = (self.balance - self.reserve())
        return max(value, 0)

    def allocate(self, percent):
        percent = max(0, min(percent, 100))
        return (self.tradable_balance() * percent / 100)

    def update_balance(self, pnl):
        self.balance += float(pnl)
        return self.balance

    def roi(self):

        if self.initial_balance <= 0:
            return 0
        return ((self.balance - self.initial_balance) / self.initial_balance) * 100

    def loss_percent(self):
        if self.initial_balance <= 0:
            return 0
        if self.balance >= self.initial_balance:
            return 0
        return ((self.initial_balance - self.balance) / self.initial_balance) * 100

    def profit_percent(self):
        if self.initial_balance <= 0:
            return 0
        if self.balance <= self.initial_balance:
            return 0
        return ((self.balance - self.initial_balance) / self.initial_balance) * 100

    def reset(self):
        self.balance = self.initial_balance

    def summary(self):
        return {"initial_balance":round(self.initial_balance, 2),
                "balance":round(self.balance, 2),
                "reserve":round(self.reserve(), 2),
                "tradable_balance":round(self.tradable_balance(), 2),
                "roi":round(self.roi(),2),
                "profit_percent":round(self.profit_percent(), 2),
                "loss_percent":round(self.loss_percent(), 2)}