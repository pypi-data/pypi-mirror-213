import json

import requests

from typing import List, Dict, Any


class AccoutningAPI:
    """Accoutning API to work with the accoutning server"""

    def __init__(self, base_url: str, currency_server_token) -> None:
        """Init the class"""
        self.base_url = base_url
        self.currenncy_server_token = currency_server_token

    def create_accoutning(self, accoutning_name: str):
        """Create the accounting"""
        import logging

        body = {"api_token": self.currenncy_server_token, "name": accoutning_name}
        response = requests.post(f"{self.base_url}/accounting", json=body)
        logging.debug(f"{response}")
        return json.loads(response.text)

    def create_contract(
        self,
        name: str,
        currency: str,
        payment_rate: int,
        timestamp_start: int,
        timestamp_end: int,
        tot_amount: int,
        type_work: Dict[str, Any],
    ):
        """Create the accounting"""
        import logging

        body = {
            "name": name,
            "currency": currency,
            "payment_rate": payment_rate,
            "timestamp_start": timestamp_start,
            "timestam_end": timestamp_end,
            "tot_amount": tot_amount,
            "type_work": type_work,
        }
        response = requests.post(f"{self.base_url}/contract", json=body)
        logging.debug(f"{response.text}")
        return json.loads(response.text)

    def calculate_report(
        self,
        name: str,
        base_currency: str,
    ):
        """Create the accounting"""
        import logging

        body = {
            "accoutning_name": name,
            "base_currency": base_currency,
        }
        response = requests.post(f"{self.base_url}/accoutning/report", json=body)
        logging.debug(f"{response.text}")
        return json.loads(response.text)

    def add_cashflow(
        self,
        name: str,
        incoming: List[Dict[str, Any]],
        outcoming: List[Dict[str, Any]],
    ):
        """Create the accounting"""
        import logging

        body = {
            "accoutning_name": name,
            "incoming": incoming,
            "outcoming": outcoming,
        }
        response = requests.post(f"{self.base_url}/add_cashflows", json=body)
        logging.debug(f"{response.text}")
        return json.loads(response.text)
