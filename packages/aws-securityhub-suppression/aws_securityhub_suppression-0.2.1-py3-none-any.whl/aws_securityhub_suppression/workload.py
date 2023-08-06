from __future__ import annotations

from typing import Optional, List

from aws_securityhub_suppression import Account


class Workload:
    def __init__(self, name: str, accounts: List[Account]) -> None:
        self.__name = name
        self.__accounts = accounts

    @property
    def name(self) -> str:
        return self.__name

    @property
    def accounts(self) -> List[Account]:
        return self.__accounts

    @staticmethod
    def from_dict(data: dict, accounts: List[Account]) -> Optional[Workload]:
        # TODO: Schema validation
        if "Name" not in data:
            return None

        return Workload(name=data["Name"], accounts=accounts)
