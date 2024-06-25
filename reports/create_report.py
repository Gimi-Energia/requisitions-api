import json
import csv
from datetime import datetime


def load_json(file_path, encoding="utf-8"):
    with open(file_path, encoding=encoding) as f:
        return json.load(f)


def translate_status(status):
    translations = {
        "Pending": "Pendente",
        "Approved": "Aprovado",
        "Opened": "Aberto",
        "Denied": "Negado",
        "Canceled": "Cancelado",
    }
    return translations.get(status, status)


def convert_date(datetime_str):
    if datetime_str:
        dt = datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
        return dt.date().isoformat()
    return ""


freights = load_json("freights.json", encoding="utf-8")
contracts = load_json("contracts.json", encoding="utf-8")
users = load_json("users.json", encoding="utf-8")
departments = load_json("departments.json", encoding="utf-8")

user_dict = {user["id"]: user["email"] for user in users["results"]}
contract_dict = {contract["pk"]: contract["fields"] for contract in contracts}
department_dict = {dept["pk"]: dept["fields"]["name"] for dept in departments}

fields_csv = [
    "pk",
    "company",
    "department_name",
    "created_at_date",
    "request_date",
    "requester",
    "status",
    "approver",
    "approval_date_date",
    "cte_number",
    "contract_number",
    "control_number",
    "freight_estimated",
    "freight_consumed",
]

rows = []

for freight in freights:
    fields_data = freight["fields"]
    created_at_date = convert_date(fields_data["created_at"])
    approval_date_date = convert_date(fields_data.get("approval_date"))

    department_name = department_dict.get(fields_data["department"], fields_data["department"])

    row = {
        "pk": freight["pk"],
        "company": fields_data["company"],
        "department_name": department_name,
        "created_at_date": created_at_date,
        "request_date": fields_data["request_date"],
        "requester": user_dict.get(fields_data["requester"], ""),
        "status": translate_status(fields_data["status"]),
        "approver": user_dict.get(fields_data["approver"], ""),
        "approval_date_date": approval_date_date,
        "cte_number": fields_data["cte_number"],
    }

    if fields_data.get("contract"):
        contract = contract_dict.get(fields_data["contract"])
        if contract:
            row["contract_number"] = contract["contract_number"].replace(".", ",")
            row["control_number"] = contract["control_number"].replace(".", ",")
            row["freight_estimated"] = str(contract["freight_estimated"]).replace(".", ",")
            row["freight_consumed"] = str(contract["freight_consumed"]).replace(".", ",")
        else:
            row["contract_number"] = ""
            row["control_number"] = ""
            row["freight_estimated"] = ""
            row["freight_consumed"] = ""
    else:
        row["contract_number"] = ""
        row["control_number"] = ""
        row["freight_estimated"] = ""
        row["freight_consumed"] = ""

    rows.append(row)

output_file = "freights_data.csv"
with open(output_file, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields_csv)
    writer.writeheader()
    writer.writerows(rows)
