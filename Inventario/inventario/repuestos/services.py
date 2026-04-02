import os
import requests
from django.conf import settings

class ERPClient:
    """Client to interact with external ERP system."""
    def __init__(self):
        self.base_url = settings.ERP_API_URL.rstrip('/')
        self.api_key = settings.ERP_API_KEY
        self.headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}

    def get_stock(self):
        """Fetch stock data from ERP."""
        url = f"{self.base_url}/stock"
        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()
        return resp.json()  # Expect list of {"numero_parte": ..., "cantidad": ...}

    def update_stock(self, numero_parte, cantidad):
        """Push stock update to ERP."""
        url = f"{self.base_url}/stock/{numero_parte}"
        payload = {'cantidad': cantidad}
        resp = requests.put(url, json=payload, headers=self.headers, timeout=10)
        resp.raise_for_status()
        return resp.json()