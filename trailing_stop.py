"""
trailing_stop.py
Risk Trailing Stop Calculation
"""
from __future__ import annotations

class TrailingStop:
    def __init__(self,distance_percent=1):
        self.distance_percent = distance_percent
        
    def next_stop( self, side, current_price):
        if side == "BUY":
            return current_price * (1 - self.distance_percent / 100)
        return current_price * (1 + self.distance_percent / 100)
        
    def should_update(self, side, current_stop, current_price):
        new_stop = self.next_stop(side, current_price)
        if side == "BUY":
            return new_stop > current_stop
        return new_stop < current_stop