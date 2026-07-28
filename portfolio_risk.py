"""
portfolio_risk.py
"""
class PortfolioRisk:

    def __init__(self, max_portfolio_risk=5.0):
        self.max_portfolio_risk = float(max_portfolio_risk)

    def total_risk(self, positions):
        total = 0.0
        for position in positions:
            total += float(position.get("risk_percent", 0))
        return total

    def total_notional(self, positions):
        total = 0.0
        for position in positions:
            total += float(position.get("notional", 0))
        return total

    def total_margin(self, positions):
        total = 0.0
        for position in positions:
            total += float(position.get("margin", 0))
        return total

    def can_open(self, positions, new_risk):

        return (self.total_risk(positions) + new_risk) <= self.max_portfolio_risk

    def remaining_risk(self, positions):
        remaining = (self.max_portfolio_risk - self.total_risk(positions))
        return max(remaining, 0)

    def highest_risk_position(self, positions):
        if not positions:
            return None
        return max(positions, key=lambda item:float(item.get("risk_percent", 0)))

    def diversification_score(self, positions):
        symbols = set()
        for position in positions:
            symbols.add(position.get("symbol"))
        if not positions:
            return 0
        return round((len(symbols) / len(positions)) * 100, 2)

    def summary(self, positions):
        return {"positions":len(positions), "portfolio_risk": round(self.total_risk(positions),2),
                "remaining_risk":round(self.remaining_risk(positions), 2),
                "total_notional":round(self.total_notional(positions), 2),
                "total_margin":round(self.total_margin(positions),2),
                "diversification":self.diversification_score(positions),
                "can_open_new_trade":self.can_open(positions, 0)}