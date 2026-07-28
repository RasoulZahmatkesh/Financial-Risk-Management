"""
exposure_manager.py
"""

class ExposureManager:

    def __init__(self, max_symbol_exposure=20.0, max_side_exposure=50.0):
        self.max_symbol_exposure = float(max_symbol_exposure)
        self.max_side_exposure = float(max_side_exposure)

    def symbol_exposure(self, positions, symbol):
        exposure = 0.0
        for position in positions:
            if position.get("symbol") == symbol:
                exposure += float(position.get("exposure_percent", 0))
        return exposure

    def side_exposure(self, positions, side):
        exposure = 0.0
        side = side.upper()
        for position in positions:
            if position.get("side", "").upper() == side:
                exposure += float(position.get("exposure_percent", 0))
        return exposure

    def total_exposure(self, positions):
        return sum(float(position.get("exposure_percent", 0))
            for position in positions)

    def can_open_symbol(self, positions, symbol, exposure):
        return (self.symbol_exposure(positions, symbol) + exposure) <= self.max_symbol_exposure

    def can_open_side(self, positions, side, exposure):
        return (self.side_exposure(positions, side) + exposure) <= self.max_side_exposure

    def remaining_symbol(self, positions, symbol):
        value = (self.max_symbol_exposure - self.symbol_exposure(positions, symbol))
        return max(value, 0)

    def remaining_side(self, positions, side):
        value = (self.max_side_exposure - self.side_exposure(positions, side))
        return max(value, 0)

    def summary(self, positions):
        long_exposure = self.side_exposure(positions, "LONG")
        short_exposure = self.side_exposure(positions, "SHORT")
        return {"total_exposure":round(self.total_exposure(positions), 2),
                "long_exposure":round(long_exposure, 2),"short_exposure":round(short_exposure, 2),
                "remaining_long":round(self.remaining_side(positions, "LONG" ),2),
                "remaining_short":round(self.remaining_side(positions,"SHORT"),2)}