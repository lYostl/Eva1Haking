import json
import dns.resolver
from pathlib import Path
from datetime import datetime

class DNSScanner:
    def __init__(self, domain):
        self.domain = domain
        self.record_types = ["A", "AAAA", "CNAME", "MX", "NS", "SOA", "TXT"]

    def run_scan(self):
        resolver = dns.resolver.Resolver()
        results = {
            "domain": self.domain,
            "resolved_at": datetime.utcnow().isoformat(),
            "records": {}
        }

        for r_type in self.record_types:
            try:
                answers = resolver.resolve(self.domain, r_type)
                results["records"][r_type] = [str(a) for a in answers]
            except Exception as e:
                results["records"][r_type] = []

        Path("data_test").mkdir(exist_ok=True)
        filename = self.domain.replace(".", "_") + "_dns.json"
        with open(Path("data_test") / filename, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)

        return results

