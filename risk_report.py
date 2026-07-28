"""
risk_report.py
"""

from datetime import datetime

class RiskReport:

    def __init__(self):
        pass

    def generate(self, account, portfolio, positions, statistics, limits):
        report = {"created_at": datetime.utcnow().isoformat(), "account":self.account_section(account),
                    "portfolio":self.portfolio_section(portfolio),
                    "positions":self.positions_section(positions),
                    "statistics":self.statistics_section(statistics),
                    "limits":self.limits_section(limits),
                    "warnings":self.warnings(account, portfolio, limits),
                    "risk_score":self.risk_score(account, portfolio, limits)}
        return report

    def account_section(self, account):
        return {"balance":account.get("balance", 0), "equity": account.get("equity",0),
                "daily_loss":account.get("daily_loss", 0), "drawdown": account.get("drawdown", 0)}

    def portfolio_section(self, portfolio):
        return {"open_positions":portfolio.get("open_positions", 0),
                "portfolio_risk":portfolio.get("portfolio_risk", 0),
                "total_exposure": portfolio.get("total_exposure", 0)}

    def positions_section(self, positions):
        return positions

    def statistics_section(self, statistics):
        return statistics

    def limits_section(self, limits):
        if hasattr(limits,"summary"):
            return limits.summary()
        return limits

    def warnings(self, account, portfolio, limits):
        warnings = []
        if account.get("drawdown",0) >= limits.max_drawdown:
            warnings.append("Maximum drawdown reached.")

        if account.get("daily_loss", 0) >= limits.max_daily_loss:
            warnings.append("Daily loss limit reached.")

        if portfolio.get("portfolio_risk", 0) >= limits.max_portfolio_risk:
            warnings.append("Portfolio risk limit reached.")

        if portfolio.get("open_positions", 0) >= limits.max_open_positions:
            warnings.append("Maximum open positions reached.")
        return warnings

    def risk_score( self, account, portfolio, limits):
        score = 100
        score -= min(account.get("drawdown", 0), 40)
        score -= min(account.get("daily_loss", 0) * 2, 20)
        score -= min(portfolio.get("portfolio_risk", 0) * 5, 25)
        score -= min(portfolio.get("open_positions", 0), limits.max_open_positions)
        return max(round(score, 2), 0)

    def export_json(self, report):

        import json
        return json.dumps(report, indent=4, default=str)

    def export_dict(self, report):
        return dict(report)