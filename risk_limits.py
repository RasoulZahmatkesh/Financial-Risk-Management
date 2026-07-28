"""
risk_limits.py
"""

class RiskLimits:

    def __init__(self,
        max_daily_loss=5.0,
        max_weekly_loss=10.0,
        max_monthly_loss=20.0,
        max_drawdown=20.0,
        max_open_positions=10,
        max_symbol_positions=1,
        max_portfolio_risk=5.0,
        max_symbol_risk=2.0,
        max_leverage=20):
        self.max_daily_loss = float(max_daily_loss)
        self.max_weekly_loss = float(max_weekly_loss)
        self.max_monthly_loss = float(max_monthly_loss)
        self.max_drawdown = float(max_drawdown)
        self.max_open_positions = int(max_open_positions)
        self.max_symbol_positions = int(max_symbol_positions)
        self.max_portfolio_risk = float(max_portfolio_risk)
        self.max_symbol_risk = float(max_symbol_risk)
        self.max_leverage = int(max_leverage)

    def check_daily_loss(self, loss_percent):
        return loss_percent <= self.max_daily_loss

    def check_weekly_loss(self, loss_percent):
        return loss_percent <= self.max_weekly_loss

    def check_monthly_loss(self, loss_percent):
        return loss_percent <= self.max_monthly_loss

    def check_drawdown(self, drawdown):
        return drawdown <= self.max_drawdown

    def check_open_positions(self, count):
        return count <= self.max_open_positions
    
    def check_symbol_positions(self, count):
        return count <= self.max_symbol_positions

    def check_portfolio_risk(self, risk):
        return risk <= self.max_portfolio_risk

    def check_symbol_risk(self, risk):
        return risk <= self.max_symbol_risk

    def check_leverage(self, leverage):
        return leverage <= self.max_leverage

    def summary(self):
        return {"max_daily_loss":self.max_daily_loss,
                "max_weekly_loss":self.max_weekly_loss,
                "max_monthly_loss":self.max_monthly_loss,
                "max_drawdown": self.max_drawdown,
                "max_open_positions": self.max_open_positions,
                "max_symbol_positions":self.max_symbol_positions,
                "max_portfolio_risk": self.max_portfolio_risk,
                "max_symbol_risk": self.max_symbol_risk,
                "max_leverage": self.max_leverage}