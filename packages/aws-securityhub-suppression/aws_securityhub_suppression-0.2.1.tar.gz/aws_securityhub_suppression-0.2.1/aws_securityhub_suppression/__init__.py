from typing import List, Optional
import glob
import os
import yaml
from aws_securityhub_suppression.account import Account
from aws_securityhub_suppression.workload import Workload
from aws_securityhub_suppression.suppression import Suppression


__version__ = "0.2.1"


def load_workloads(workload_path: str) -> List[Workload]:
    workloads = glob.glob(os.path.join(workload_path, "**/info.yaml"), recursive=True)

    def load_workload(file: str) -> Optional[Workload]:
        return load_workload_by_file(file)

    response = list(map(load_workload, workloads))

    return list(filter(None, response))


def load_accounts_by_file(path: str) -> Optional[Account]:
    with open(path, "r") as f:
        return Account.from_dict(yaml.safe_load(f))


def load_workload_by_file(path: str) -> Optional[Workload]:
    workload_base = os.path.dirname(path)
    accounts_files = glob.glob(os.path.join(workload_base, "*.yaml"), recursive=True)
    accounts_files = [file for file in accounts_files if not file.endswith("info.yaml")]
    response = list(map(load_accounts_by_file, accounts_files))
    accounts = list(filter(None, response))

    with open(path, "r") as f:
        return Workload.from_dict(yaml.safe_load(f), accounts)
