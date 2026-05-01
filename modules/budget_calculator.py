from dataclasses import dataclass, field
from typing import Dict, List


# -----------------------------
# LABOR DATA MODELS
# -----------------------------

@dataclass
class LaborRole:
    name: str
    hourly_rate: float
    overtime_rate: float
    payroll_tax_rate: float = 0.075  # 7.5% default
    benefit_rate: float = 0.20       # 20% default


@dataclass
class LaborData:
    role: LaborRole
    hours: float
    overtime_hours: float = 0

    def total_cost(self) -> float:
        base = self.hours * self.role.hourly_rate
        overtime = self.overtime_hours * self.role.overtime_rate
        taxes = (base + overtime) * self.role.payroll_tax_rate
        benefits = (base + overtime) * self.role.benefit_rate
        return base + overtime + taxes + benefits


# -----------------------------
# BUDGET CATEGORY MODELS
# -----------------------------

@dataclass
class BudgetItem:
    name: str
    amount: float  # monthly or annual depending on your app


@dataclass
class BudgetCategory:
    name: str
    items: List[BudgetItem] = field(default_factory=list)

    def total(self) -> float:
        return sum(item.amount for item in self.items)


# -----------------------------
# MAIN BUDGET CALCULATOR
# -----------------------------

@dataclass
class DistributionCenterBudget:
    labor_data: List[LaborData] = field(default_factory=list)
    categories: Dict[str, BudgetCategory] = field(default_factory=dict)

    # ---- LABOR COSTS ----
    def total_labor_cost(self) -> float:
        return sum(l.total_cost() for l in self.labor_data)

    # ---- NON-LABOR COSTS ----
    def total_non_labor_cost(self) -> float:
        return sum(cat.total() for cat in self.categories.values())

    # ---- TOTAL DC COST ----
    def total_cost(self) -> float:
        return self.total_labor_cost() + self.total_non_labor_cost()

    # ---- COST PER UNIT ----
    def cost_per_unit(self, units_processed: int) -> float:
        if units_processed == 0:
            return 0
        return self.total_cost() / units_processed

    # ---- VARIANCE ----
    def variance(self, actual_cost: float) -> float:
        return actual_cost - self.total_cost()

    # ---- FORECASTING ----
    def forecast_labor_cost(self, growth_rate: float) -> float:
        return self.total_labor_cost() * (1 + growth_rate)
