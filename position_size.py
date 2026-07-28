"""
position_sizer.py
"""

class PositionSizer:

    def __init__(self):
        pass

    def fixed_risk(self, balance, risk_percent, entry, stop):
        risk_amount = (balance * risk_percent / 100)
        stop_distance = abs(entry - stop)
        if stop_distance <= 0:
            raise ValueError("Invalid stop distance")
        return risk_amount / stop_distance

    def fixed_amount(self, amount):
        return amount

    def fixed_percent(self, balance, percent,price):
        capital = (balance * percent / 100)
        return capital / price

    def kelly(self, balance, win_rate, reward_ratio, price):
        p = win_rate
        q = 1 - p
        edge = (p * reward_ratio - q) / reward_ratio
        if edge <= 0:
            return 0
        capital = balance * edge
        return capital / price

    def volatility(self, balance, atr, multiplier, price):
        risk = atr * multiplier
        if risk <= 0:
            return 0
        return (balance / risk) / price