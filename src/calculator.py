#!/usr/bin/env python3

from datetime import datetime

# Constants
INFLATION_RATE = 0.03
SALARY_INCREASE_RATE = 0.02


def present_value_annuity(payment, rate, periods) -> float:
    """
    Calculate present value of an annuity.

    Parameters:
    payment (float): Amount of each payment.
    rate (float): Interest rate per period (decimal).
    periods (int): Number of periods.

    Returns:
    float: Present value of the annuity.
    """
    return payment * ((1 - (1 + rate) ** -periods) / rate)


def future_value_lump_sum(principal, rate, periods) -> float:
    """
    Calculate future value of a lump sum investment.

    Parameters:
    principal (float): Initial amount.
    rate (float): Interest rate per period (decimal).
    periods (int): Number of periods.

    Returns:
    float: Future value of the investment.
    """
    return principal * ((1 + rate) ** periods)


def calculate_retirerment_savings(
    dob: datetime,
    household_income: float,
    current_savings_rate: float,
    current_retirement_savings: float,
    pre_retirement_income_percent: float,
    life_expectancy: int,
    expected_rate_of_return: float,
    retirement_age: int,
) -> tuple[float, float]:
    """
    Calculate the amount needed to retire and the expected total savings at retirement age.

    Parameters:
    dob (datetime): Date of birth.
    household_income (float): Annual household income.
    current_savings_rate (float): Current savings rate (decimal).
    current_retirement_savings (float): Current retirement savings.
    pre_retirement_income_percent (float): Percent of income needed in retirement (decimal).
    life_expectancy (int): Life expectancy.
    expected_rate_of_return (float): Expected rate of return (decimal).
    retirement_age (int): Retirement age.

    Returns:
    tuple[float, float]: (amount needed to retire, expected total savings at retirement age)
    """

    # Current age and years until retirement
    current_date = datetime.now()
    current_age = (
        current_date.year - dob.year - (
            # if current date is before the birthday in the current year,
            # we must subtract one year from the age
            (current_date.month, current_date.day) < (dob.month, dob.day)
        )
    )

    years_until_retirement = retirement_age - current_age
    years_in_retirement = life_expectancy - retirement_age

    # Calculate amount Needed to Retire
    # Annual retirement expenses adjusted for inflation
    annual_retirement_expenses = household_income * pre_retirement_income_percent
    adjusted_annual_expenses = annual_retirement_expenses * (
        (1 + INFLATION_RATE) ** years_until_retirement
    )

    # Calculate amount needed to retire (Present Value of Annuity)
    adjusted_annual_expenses = annual_retirement_expenses * (
        (1 + INFLATION_RATE) ** years_until_retirement
    )

    amount_needed_to_retire = present_value_annuity(
        adjusted_annual_expenses, INFLATION_RATE, years_in_retirement
    )

    # Calculate expected amount saved by retirement age (Future Value of Lump Sum and Series)
    future_value_current_savings = future_value_lump_sum(
        current_retirement_savings, expected_rate_of_return, years_until_retirement
    )

    # Future value of annual savings
    annual_savings = household_income * current_savings_rate
    future_value_annual_savings = 0
    for year in range(years_until_retirement):
        future_value_annual_savings += future_value_lump_sum(
            annual_savings, expected_rate_of_return, years_until_retirement - year
        )
        annual_savings *= 1 + SALARY_INCREASE_RATE

    # Total amount expected to be saved
    expected_total_savings = future_value_current_savings + future_value_annual_savings

    return (amount_needed_to_retire, expected_total_savings)
