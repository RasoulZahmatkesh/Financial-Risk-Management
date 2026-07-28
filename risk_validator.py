"""
risk_validator.py
"""

from risk.risk_limits import RiskLimits

class RiskValidator:

    def __init__(self, limits=None):
        self.limits = limits or RiskLimits()

    def validate_trade(self, trade, portfolio):
        errors = []

        if not self.limits.check_leverage(
            trade.get("leverage", 1)):
            errors.append("Maximum leverage exceeded.")

        if not self.limits.check_symbol_risk(trade.get(
                "risk_percent", 0)):
            errors.append("Symbol risk limit exceeded.")
        portfolio_risk = portfolio.get("portfolio_risk", 0)

        if not self.limits.check_portfolio_risk(portfolio_risk):
            errors.append("Portfolio risk limit exceeded.")

        if not self.limits.check_open_positions(portfolio.get("open_positions", 0)):
            errors.append("Maximum open positions reached.")

        symbol_positions = portfolio.get("symbol_positions", 0)

        if not self.limits.check_symbol_positions(symbol_positions):
            errors.append("Maximum symbol positions reached.")

        return {"valid":len(errors) == 0, "errors": errors}

    def validate_account(self, account):
        errors = []

        if not self.limits.check_daily_loss(account.get("daily_loss", 0)):
            errors.append("Daily loss limit exceeded.")

        if not self.limits.check_weekly_loss(account.get("weekly_loss", 0)):
            errors.append("Weekly loss limit exceeded.")

        if not self.limits.check_monthly_loss(
            account.get("monthly_loss", 0)):
            errors.append( "Monthly loss limit exceeded.")

        if not self.limits.check_drawdown(account.get("drawdown", 0)):
            errors.append("Maximum drawdown exceeded.")

        return {"valid":len(errors) == 0, "errors": errors}

    def validate_all(self, trade, portfolio, account):
        trade_result = self.validate_trade(trade, portfolio)
        account_result = self.validate_account(account)
        errors = (trade_result["errors"] + account_result["errors"])
        return {"valid": len(errors) == 0, "errors": errors}