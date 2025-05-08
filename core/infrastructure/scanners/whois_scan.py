import whois
from datetime import datetime
from pathlib import Path
import json

class WhoisScanner:
    def __init__(self, domain):
        self.domain = domain

    def run_scan(self):
        try:
            w = whois.whois(self.domain)
            results = {
                "domain": self.domain,
                "scanned_at": datetime.utcnow().isoformat(),
                "whois": {
                    "registrar": w.registrar,
                    "creation_date": str(w.creation_date),
                    "expiration_date": str(w.expiration_date),
                    "updated_date": str(w.updated_date),
                    "name_servers": w.name_servers,
                    "emails": w.emails,
                    "country": w.country,
                    "status": w.status,
                    "whois_server": w.whois_server
                }
            }
        except Exception as e:
            results = {"error": str(e)}

        Path("data_test").mkdir(exist_ok=True)
        path = Path("data_test") / (self.domain.replace(".", "_") + "_whois.json")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)

        return results
