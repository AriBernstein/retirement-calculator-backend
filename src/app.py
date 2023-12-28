#!/usr/bin/env python3

import requests
from datetime import datetime
from calculator import calculate_retirerment_savings

USER_ENDPOINT_URI = "https://pgf7hywzb5.execute-api.us-east-1.amazonaws.com/users"


def query_user_info(user_id) -> dict:
    """
    Queries the specified endpoint with a user ID and returns the user information.

    Args:
    user_id (int): The user ID to query the endpoint with.

    Returns:
    dict: A dictionary containing the user information from the response.
    """
    url = f"{USER_ENDPOINT_URI}/{user_id}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()

        raise Exception(
            f"Failed to retrieve data: HTTP status code {response.status_code}"
        )

    except requests.RequestException as e:
        raise Exception(f"An error occurred while making the request: {e}")


def get_retirement_savings_str(user_id: int) -> str:
    """
    Returns a string containing the retirement savings information for the specified user.

    Args:
    user_id (int): The user ID to query the endpoint with.

    Returns:
    str: A string containing the retirement savings information for the specified user.

    Raises:
    ValueError: If the user_id is not an integer.
    Exception: For failed requests or non-200 HTTP responses.
    """

    if not isinstance(user_id, int):
        raise ValueError("User ID must be an integer")
    if int(user_id) < 0:
        raise ValueError("User ID must be a positive integer")

    payload = query_user_info(user_id)
    user_info = payload["user_info"]
    user_assumptions = payload["assumptions"]

    amount_needed_to_retire, expected_total_savings = calculate_retirerment_savings(
        datetime.strptime(user_info["date_of_birth"], "%Y-%m-%d"),
        user_info["household_income"],
        int(user_info["current_savings_rate"]) / 100,
        user_info["current_retirement_savings"],
        int(user_assumptions["pre_retirement_income_percent"]) / 100,
        user_assumptions["life_expectancy"],
        int(user_assumptions["expected_rate_of_return"]) / 100,
        user_assumptions["retirement_age"],
    )

    dollar_approximate = lambda x: "{:,}".format(int(round(x, -3)))

    return (
        f"To retire at age {user_assumptions['retirement_age']}:"
        f"\nYou will need ${dollar_approximate(amount_needed_to_retire)}"
        f"\nYou will have saved ${dollar_approximate(expected_total_savings)}"
    )
