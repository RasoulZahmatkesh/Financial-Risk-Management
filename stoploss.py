"""
stoploss.py
Risk Stop Loss Calculation
"""
from __future__ import annotations

class StopLoss:
    @staticmethod
    def fixed(entry_price, percent, side):
        if side == "BUY":
            return entry_price * (1 - percent / 100)
        return entry_price * (1 + percent / 100)
        
    @staticmethod
    def atr(entry_price, atr, multiplier, side):
        distance = atr * multiplier
        if side == "BUY":
            return entry_price - distance
        return entry_price + distance
    
    @staticmethod
    def candle(candle_low, candle_high, side):
        if side == "BUY":
            return candle_low
        return candle_high
    
    @staticmethod
    def risk_amount(balance, risk_percent):
        return (balance * risk_percent / 100)