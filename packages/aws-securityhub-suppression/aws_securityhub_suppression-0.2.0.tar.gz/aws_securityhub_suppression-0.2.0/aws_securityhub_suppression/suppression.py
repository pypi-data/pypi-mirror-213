from __future__ import annotations
from typing import Optional, List, Any

from aws_securityhub_suppression.finding import Finding


class Suppression:
    def __init__(self, name: str, reason: str, findings: List[Finding]) -> None:
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
    def findings(self) -> List[Finding]:
        return self.__findings

    @staticmethod
    def from_dict(data: dict) -> Optional[Suppression]:
        # TODO: Schema validation
        if "Name" not in data:
            return None

        findings = list(map(Finding, data["Findings"]))

        return Suppression(name=data["Name"], reason=data["Reason"], findings=findings)
