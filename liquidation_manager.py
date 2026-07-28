"""
liquidation_manager.py
"""
class LiquidationManager:

    def __init__(self, maintenance_margin_rate=0.005):
        self.maintenance_margin_rate = (maintenance_margin_rate)

    def maintenance_margin(self, position_value):
        return (
            position_value *
            self.maintenance_margin_rate)

    def long_price(self, entry_price, leverage, maintenance_margin_rate=None):
        mmr = (maintenance_margin_rate
            if maintenance_margin_rate is not None
            else self.maintenance_margin_rate)
        leverage = max(leverage, 1)
        return entry_price * (1 -(1 / leverage) + mmr)
    
    def short_price(self,entry_price, leverage, maintenance_margin_rate=None):
        mmr = (maintenance_margin_rate
            if maintenance_margin_rate is not None
            else self.maintenance_margin_rate)
        leverage = max(leverage, 1)
        return entry_price * (1 + (1 / leverage) - mmr)

    def liquidation_price(self, direction, entry_price, leverage):
        if direction.upper() == "LONG":
            return self.long_price(entry_price, leverage)
        return self.short_price(entry_price, leverage)

    def distance(self, current_price, liquidation_price):
        return abs(current_price - liquidation_price)

    def distance_percent(self, current_price, liquidation_price):
        if current_price <= 0:
            return 0
        return (abs(current_price - liquidation_price) / current_price) * 100

    def is_danger(self, current_price, liquidation_price, warning_percent=10):
        return (self.distance_percent(current_price, liquidation_price) <= warning_percent)

    def is_liquidated(self, direction, current_price, liquidation_price):
        if direction.upper() == "LONG":
            return ( current_price <= liquidation_price)
        return (current_price >= liquidation_price)

    def summary(self, direction, entry_price, current_price, leverage):
        liq = self.liquidation_price(direction, entry_price, leverage)
        return {"entry_price": entry_price, "current_price": current_price, "liquidation_price": liq,
                "distance": self.distance(current_price, liq), "distance_percent": round(self.distance_percent(current_price, liq), 2),
                "danger": self.is_danger(current_price, liq),
                "liquidated": self.is_liquidated(direction, current_price, liq)}