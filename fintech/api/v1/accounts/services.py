from typing import NamedTuple, Optional


class CreateAccountData(NamedTuple):
    account_number: str
    currency: str
    amount: Optional[float]


class CreateAccountService:
    pass