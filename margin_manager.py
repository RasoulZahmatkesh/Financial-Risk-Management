"""
margin_manager.py
"""

class MarginManager:

    def __init__(self, maintenance_margin=0.005):
        self.maintenance_margin = maintenance_margin

    def initial_margin(self, position_value, leverage):
        leverage = max(leverage, 1)
        return (position_value / leverage)

    def maintenance(self, position_value):
        return (position_value * self.maintenance_margin)

    def free_margin(self, balance, used_margin):
        return (balance - used_margin)

    def margin_level(self, equity, used_margin):
        if used_margin <= 0:
            return float("inf")
        return (equity / used_margin) * 100

    def can_open(self, balance, position_value, leverage):
        required = self.initial_margin(position_value, leverage)
        return balance >= required
    
    def used_margin(self, positions):
        total = 0
        for position in positions:
            total += position.get("margin", 0)
        return total

    def available_margin(self, balance, positions):
        return self.free_margin(balance, self.used_margin(positions))

    def margin_call(self, equity, used_margin, threshold=100):
        level = self.margin_level(equity, used_margin)
        return level <= threshold

    def stop_out(self, equity, used_margin, threshold=50):
        level = self.margin_level(equity, used_margin)
        return level <= threshold

    def summary(self, balance, equity, positions):
        used = self.used_margin(positions)
        free = self.free_margin(equity, used)
        level = self.margin_level(equity, used)
        return {"balance": balance, "equity": equity, "used_margin": used, "free_margin": free,
                "margin_level": level, "margin_call": self.margin_call(equity, used),
                "stop_out": self.stop_out(equity, used)}