"""
correlation_manager.py
"""

from itertools import combinations
import pandas as pd

class CorrelationManager:

    def __init__(self, max_correlation=0.80):
        self.max_correlation = float(max_correlation)

    def matrix(self,price_data):

        """price_data:
        {"BTC/USDT": Series,"ETH/USDT": Series,...}
        """
        df = pd.DataFrame(price_data)
        return df.corr(method="pearson")
    
    def correlation(self, price_data, symbol1, symbol2):
        corr = self.matrix(price_data)
        return float(corr.loc[symbol1, symbol2])

    def highly_correlated(self, price_data):
        corr = self.matrix(price_data)
        result = []
        for a, b in combinations(corr.columns, 2):
            value = abs(corr.loc[a, b])
            if value >= self.max_correlation:
                result.append({"symbol1": a, "symbol2": b, "correlation": round(value, 4)})
        return result
    def can_open(self, symbol, opened_symbols, price_data):
        if symbol not in price_data:
            return True
        corr = self.matrix(price_data)
        for opened in opened_symbols:
            if opened not in corr.columns:
                continue
            value = abs(corr.loc[symbol, opened])
            if value >= self.max_correlation:
                return False
        return True

    def portfolio_score(self, opened_symbols, price_data):
        if len(opened_symbols) < 2:
            return 100.0
        corr = self.matrix(price_data)
        values = []
        for a, b in combinations(opened_symbols, 2):
            if (a in corr.columns and b in corr.columns):
                values.append(abs(corr.loc[a, b]))
        if not values:
            return 100.0
        avg = sum(values) / len(values)
        return round((1 - avg) * 100, 2)

    def summary(self, opened_symbols, price_data):
        return {"max_allowed_correlation":self.max_correlation,
                "portfolio_score":self.portfolio_score(opened_symbols, price_data),
                "highly_correlated_pairs":self.highly_correlated(price_data)}