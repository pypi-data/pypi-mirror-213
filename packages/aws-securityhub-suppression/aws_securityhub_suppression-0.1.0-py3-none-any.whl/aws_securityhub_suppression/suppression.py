from __future__ import annotations
from typing import Optional, List


class Suppression:
    def __init__(self, name: str, reason: str, findings: List[str]) -> None:
        self.__name = name
        self.__reason = reason
        self.__findings = findings

    @property
    def name(self) -> str:
        return self.__name

    @property
    def reason(self) -> str:
        return self.__reason

    @property
    def findings(self) -> List[str]:
        return self.__findings

    @staticmethod
    def from_dict(data: dict) -> Optional[Suppression]:
        # TODO: Schema validation
        if "Name" not in data:
            return None

        return Suppression(
            name=data["Name"], reason=data["Reason"], findings=data["Findings"]
        )
