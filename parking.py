import argparse
import os
from datetime import date

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://haringey.tarantopermits.com"
LOGIN_URL = BASE_URL + "/Permits/Account/Login"
VOUCHERS_URL = BASE_URL + "/Permits/Permits/BuyUseVouchers"
USERNAME = os.environ["HARINGEY_USERNAME"]
PASSWORD = os.environ["HARINGEY_PASSWORD"]
CAR_REG = os.environ["HARINGEY_CAR_REG"]

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("date", type=date.fromisoformat)
args = arg_parser.parse_args()
on_date: str = args.date.strftime("%d/%m/%Y")

session = requests.Session()
print("Get login page...")
response = session.get(LOGIN_URL)
response.raise_for_status()

token = ""
for input_element in BeautifulSoup(response.text, "html.parser").find_all("input"):
    if not input_element.has_attr("name"):
        continue
    if input_element.attrs["name"] == "__RequestVerificationToken":
        token = input_element.attrs["value"]

if not token:
    raise ValueError("No token found from initial request")

print("Send login data")
response = session.post(
    LOGIN_URL,
    data={
        "Username": USERNAME,
        "Password": PASSWORD,
        "__RequestVerificationToken": token,
    },
)
response.raise_for_status()

voucher_purchase_data = {
    "Action": "Activate",
    "Reference": "",
    "Code": "0",
    "VouchersAvailable.ActivatingPermit": "1",
    "VouchersAvailable.BuyString": "1",
    "VouchersAvailable.EndDateOnly": f"{on_date} 00:00:00",
    "VouchersAvailable.EndDateTime": f"{on_date} 16:00",
    "VouchersAvailable.SelectedLocation": "Bruce Grove West (BGW)",
    "VouchersAvailable.SelectedVRM": "RE53YWO",
    "VouchersAvailable.StartDateOnly": f"{on_date} 00:00:00",
    "VouchersAvailable.StartDateTime": f"{on_date} 14:00",
    "VouchersAvailable.IsVisitorActivation": "False",
    "VouchersPrePaid.BuyString": "",
    "VouchersPrePaid.FormPreReadPermitReferences": "",
    "VouchersPrePaid.PermitCount": "2",
    "VoucherPreRequisiteMessage": "Unfortunately, you do not qualify to buy visitor / short stay voucher permits – only qualified residents and some Essential Service customers are eligible.  Please visit our website for details.",
    "hdnBuyingTandCPermitType": "",
    "hdnMustReadAll": "0",
    "chkTandCAccept": "false",
}
print("Buy vouchers")
response = session.post(
    VOUCHERS_URL,
    data=voucher_purchase_data,
)
response.raise_for_status()
