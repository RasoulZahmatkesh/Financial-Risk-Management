"""
drawdown_manager.py
"""
class DrawdownManager:

    def __init__(self, max_drawdown_percent=20):
        self.max_drawdown_percent = (max_drawdown_percent)
        self.initial_balance = None
        self.peak_balance = None

    def start(self, balance):
        self.initial_balance = float(balance)
        self.peak_balance = float(balance)

    def update(self, balance):
        balance = float(balance)
        if self.initial_balance is None:
            self.start(balance)
        if balance > self.peak_balance:
            self.peak_balance = balance
        return self.current_drawdown(balance)

    def current_drawdown(self, balance):
        if self.peak_balance <= 0:
            return 0
        return ((self.peak_balance - balance) / self.peak_balance) * 100

    def total_drawdown(self, balance):
        if self.initial_balance <= 0:
            return 0
        return ((self.initial_balance - balance) / self.initial_balance) * 100

    def allowed(self, balance):
        return (self.current_drawdown(balance) < self.max_drawdown_percent)

    def should_stop(self, balance):
        return not self.allowed(balance)

    def remaining(self, balance):
        value = (self.max_drawdown_percent - self.current_drawdown(balance))
        return max(value, 0)
    def reset(self, balance):
        self.start(balance)

    def summary(self, balance):
        return {"initial_balance":self.initial_balance,
                "peak_balance":self.peak_balance,
                "current_balance":balance,
                "drawdown_percent":round(self.current_drawdown(balance), 2),
                "total_drawdown":round(self.total_drawdown(balance), 2),
                "max_allowed":self.max_drawdown_percent,
                "remaining":round(self.remaining(balance),2),
                "trading_allowed":self.allowed(balance)}