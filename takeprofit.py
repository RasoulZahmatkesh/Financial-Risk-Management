"""
takeprofit.py
Risk Take Profit Calculation
"""

from __future__ import annotations

class TakeProfit:
    @staticmethod
    def fixed(entry_price, percent, side):
        if side == "BUY":
            return entry_price * (1 + percent / 100)
        return entry_price * (1 - percent / 100)
        
    @staticmethod
    def risk_reward(entry, stop, rr, side):
        risk = abs(entry - stop)
        reward = risk * rr
        if side == "BUY":
            return entry + reward
        return entry - reward
    
    @staticmethod
    def multiple_targets( entry, stop, side, targets=(1, 2, 3)):
        risk = abs(entry - stop)
        levels = []
        for rr in targets:
            if side == "BUY":
                levels.append(entry + risk * rr)
            else:
                levels.append(entry - risk * rr)
        return levels