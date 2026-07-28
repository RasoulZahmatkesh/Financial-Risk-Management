"""
leverage_manager.py
"""
class LeverageManager:

    def __init__(self, exchange=None, default_leverage=1, max_leverage=125):
        self.exchange = exchange
        self.default_leverage = default_leverage
        self.max_leverage = max_leverage

    def validate(self, leverage):
        leverage = int(leverage)
        if leverage < 1:
            leverage = 1
        if leverage > self.max_leverage:
            leverage = self.max_leverage
        return leverage

    def calculate_position_value(self, balance, leverage):
        leverage = self.validate(leverage)
        return balance * leverage

    def margin_required(self, position_value, leverage):
        leverage = self.validate(leverage)
        return (position_value / leverage)

    def recommended(self, risk_percent):
        if risk_percent <= 0.5:
            return 20
        if risk_percent <= 1:
            return 10
        if risk_percent <= 2:
            return 5
        return 2

    def set_exchange_leverage(self, symbol, leverage):
        leverage = self.validate(leverage)
        if self.exchange is None:
            return leverage
        if hasattr(self.exchange, "set_leverage"):
            return self.exchange.set_leverage(leverage, symbol)
        return leverage

    def current(self, symbol):
        if self.exchange is None:
            return self.default_leverage
        if hasattr(self.exchange, "fetch_positions"):
            positions = self.exchange.fetch_positions()
            for position in positions:
                if position.get("symbol") == symbol:
                    return int(position.get("leverage", self.default_leverage))
        return self.default_leverage

    def increase(self, current, step=1):
        return self.validate(current + step)

    def decrease(self, current, step=1):
        return self.validate(current - step)

    def max_position_size(self, balance, leverage, price):
        value = self.calculate_position_value(balance,leverage)
        return value / price

    def liquidation_buffer(self, leverage):
        leverage = self.validate(leverage)
        return max(100 / leverage, 0.5)