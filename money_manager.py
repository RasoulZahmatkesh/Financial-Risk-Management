"""
money_manager.py
"""

from dataclasses import dataclass

@dataclass
class MoneyManagementResult:
    risk_amount: float
    position_size: float
    stop_distance: float
    reward_distance: float
    take_profit: float
    reward_ratio: float

class MoneyManager:

    def __init__(self, default_risk_percent=1.0, max_risk_percent=2.0, min_risk_percent=0.25):
        self.default_risk_percent = float(default_risk_percent)
        self.max_risk_percent = float(max_risk_percent)
        self.min_risk_percent = float(min_risk_percent)

    def normalize_risk(self, risk_percent):

        risk = float(risk_percent)
        risk = max(self.min_risk_percent, risk)
        risk = min(self.max_risk_percent,risk)
        return risk

    def risk_amount(self, balance, risk_percent):
        risk = self.normalize_risk(risk_percent)
        return (balance * risk / 100)

    def position_size(self, balance, risk_percent, entry_price, stop_loss):
        stop_distance = abs(entry_price - stop_loss)

        if stop_distance <= 0:
            raise ValueError("Invalid stop distance")
        risk = self.risk_amount(balance, risk_percent)
        return risk / stop_distance

    def take_profit(self, entry_price, stop_loss, reward_ratio, side):
        distance = abs(entry_price - stop_loss)
        reward = (distance * reward_ratio)
        side = side.upper()
        if side == "LONG":
            return entry_price + reward
        return entry_price - reward

    def calculate(self, balance, risk_percent, entry_price, stop_loss, reward_ratio, side):
        risk = self.risk_amount(balance, risk_percent)
        size = self.position_size(balance, risk_percent, entry_price, stop_loss)
        stop_distance = abs(entry_price - stop_loss)
        reward_distance = (stop_distance * reward_ratio)
        tp = self.take_profit(entry_price, stop_loss, reward_ratio, side)
        return MoneyManagementResult(risk_amount=risk, position_size=size, stop_distance=stop_distance,
                    reward_distance=reward_distance, take_profit=tp, reward_ratio=reward_ratio)

    def scale_after_win(self, risk_percent, increase=0.10):
        return self.normalize_risk(risk_percent * ( 1 + increase))

    def scale_after_loss(self, risk_percent, decrease=0.10):
        return self.normalize_risk(risk_percent * ( 1 - decrease))

    def fixed_lot(self, lot):
        return float(lot)