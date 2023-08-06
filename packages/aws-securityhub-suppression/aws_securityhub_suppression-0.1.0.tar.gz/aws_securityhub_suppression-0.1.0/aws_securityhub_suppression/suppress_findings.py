from typing import List

from aws_securityhub_suppression import Workload
from aws_securityhub_suppression.suppression import Suppression


class SuppressFindings:
    def __init__(self, client, workload: Workload) -> None:
        self.__client = client
        self.__workload = workload

    def execute(self):
        for account in self.__workload.accounts:
            suppress_findings = account.scheduled_for_suppression()
            self.__handle_suppressions(suppress_findings)

    def __handle_suppressions(self, suppressions: List[Suppression]) -> None:
        def parse_arn(arn: str) -> dict:
            parts = arn.split(":")
            return {
                "Partition": parts[1],
                "Service": parts[2],
                "Region": parts[3],
                "AccountId": parts[4],
                "Type": parts[5],
            }

        def convert_to_finding_identifier(finding_id: str) -> dict:
            arn = parse_arn(finding_id)
            return {
                "Id": finding_id,
                "ProductArn": f"arn:aws:securityhub:{arn['Region']}::product/aws/securityhub",
            }

        for suppression in suppressions:
            finding_identifiers = list(
                map(convert_to_finding_identifier, suppression.findings)
            )

            self.__client.batch_update_findings(
                FindingIdentifiers=finding_identifiers,
                Note={
                    "Text": suppression.reason,
                    "UpdatedBy": "Cloud Center of Excellence",
                },
                Workflow={"Status": "SUPPRESSED"},
            )
