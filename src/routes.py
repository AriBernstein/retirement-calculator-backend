#!/usr/bin/env python3

from fastapi import APIRouter, HTTPException
from app import get_retirement_savings_str

router = APIRouter()


@router.get(
    "/retirement_calculator/{user_id}",
    description=(
        "Get projected amount needed for retirement and savings "
        "at retirement age for user with user_id"
    ),
)
async def get_retirement_savings(user_id: int) -> str:
    try:
        return get_retirement_savings_str(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
