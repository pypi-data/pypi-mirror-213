from __future__ import annotations
from typing import Optional, List

import landingzone_organization

from aws_securityhub_suppression.suppression import Suppression


class Account(landingzone_organization.Account):
    def __init__(
        self, name: str, account_id: str, suppressions: List[Suppression]
    ) -> None:
        super().__init__(name, account_id)
        self.__suppressions = suppressions

    @property
    def suppressions(self) -> List[Suppression]:
        return self.__suppressions

    def scheduled_for_suppression(self) -> List[Suppression]:
        # TODO: Do something clever here
        return self.suppressions

    @staticmethod
    def from_dict(data: dict) -> Optional[Account]:
        # TODO: Schema validation
        if "Name" not in data:
            return None

        suppressions = list(Suppression.from_dict(d) for d in data["Suppressions"])
        return Account(
            name=data["Name"],
            account_id=data["AccountId"],
            suppressions=list(filter(None, suppressions)),
        )
