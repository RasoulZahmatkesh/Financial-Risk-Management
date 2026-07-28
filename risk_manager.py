"""
risk_manager.py
"""

from dataclasses import dataclass


@dataclass
class RiskResult:
    balance: float
    risk_percent: float
    risk_amount: float
    entry_price: float
    stop_loss: float
    take_profit: float
    stop_distance: float
    leverage: int
    position_size: float
    reward_ratio: float
    liquidation_price: float
    margin: float

class RiskManager:
    def __init__(self):
        pass

    def calculate(self, balance, risk_percent, entry_price, stop_loss, leverage, take_profit):
        balance = float(balance)
        risk_percent = float(risk_percent)
        entry_price = float(entry_price)
        stop_loss = float(stop_loss)
        take_profit = float(take_profit)
        leverage = int(leverage)
        risk_amount = (balance * risk_percent / 100)
        stop_distance = abs(entry_price - stop_loss)

        if stop_distance <= 0:
            raise ValueError("Invalid Stop Loss")

        position_size = (risk_amount / stop_distance)
        margin = (position_size * entry_price) / leverage
        reward_ratio = abs(take_profit - entry_price) / stop_distance
        liquidation_price = self.liquidation_price(entry_price, leverage)
        return RiskResult(balance=balance, risk_percent=risk_percent, risk_amount=risk_amount,
            entry_price=entry_price, stop_loss=stop_loss, take_profit=take_profit,
            stop_distance=stop_distance, leverage=leverage, position_size=round(
            position_size, 6),
            reward_ratio=round(reward_ratio, 2),
            iquidation_price=round(liquidation_price, 4),
            margin=round(margin, 2))

    def liquidation_price(self, entry_price, leverage):
        return entry_price * (1 -(1 / leverage))

    def validate(self, balance, position_size):
        if balance <= 0:
            return False
        if position_size <= 0:
            return False
        return True

    def risk_money(self, balance, risk_percent):
        return (balance * risk_percent / 100)

    def rr(self, entry, stop, target):
        risk = abs(entry - stop)
        reward = abs(target - entry)
        if risk == 0:
            return 0
        return reward / risk

    def position_value(self, entry, amount):
        return entry * amount

    def required_margin(self, value, leverage):
        return value / leverage