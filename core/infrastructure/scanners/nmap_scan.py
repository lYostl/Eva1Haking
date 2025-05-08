import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import json

class NmapScanner:
    def __init__(self, target):
        self.target = target

    def run_scan(self):
        filename = f"/tmp/nmap_{self.target}.xml"
        results = {"target": self.target, "scanned_at": datetime.utcnow().isoformat(), "nmap": []}

        try:
            subprocess.run(
                ["nmap", "-A", "-T4", "-oX", filename, self.target],
                check=True,
                capture_output=True
            )

            tree = ET.parse(filename)
            root = tree.getroot()
            host = root.find("host")

            info = {"ip": "", "ports": []}
            address = host.find("address")
            if address is not None:
                info["ip"] = address.attrib["addr"]

            ports = host.find("ports")
            if ports is not None:
                for port in ports.findall("port"):
                    port_info = {
                        "port": port.attrib["portid"],
                        "protocol": port.attrib["protocol"],
                        "state": port.find("state").attrib["state"],
                        "service": {}
                    }
                    service = port.find("service")
                    if service is not None:
                        port_info["service"] = {
                            "name": service.attrib.get("name", ""),
                            "product": service.attrib.get("product", ""),
                            "version": service.attrib.get("version", "")
                        }
                    info["ports"].append(port_info)

            results["nmap"].append(info)
        except subprocess.CalledProcessError as e:
            results["error"] = f"Nmap error: {e}"

        Path("data_test").mkdir(exist_ok=True)
        path = Path("data_test") / (self.target.replace(".", "_") + "_nmap.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)

        return results
