import subprocess
import json
from datetime import datetime
from pathlib import Path

class NmapScanner:
    def __init__(self, target):
        self.target = target

    def run_scan(self):
        try:
            xml_output = f"/tmp/nmap_{self.target.replace('.', '_')}.xml"
            subprocess.run(
                ["nmap", "-A", "-Pn", "-T4", "-oX", xml_output, self.target],
                check=True,
                capture_output=True
            )

            import xml.etree.ElementTree as ET
            tree = ET.parse(xml_output)
            root = tree.getroot()

            host_info = {"ip": "", "ports": []}
            address = root.find("host/address")
            if address is not None:
                host_info["ip"] = address.attrib["addr"]

            for port in root.findall(".//port"):
                port_info = {
                    "port": port.attrib["portid"],
                    "protocol": port.attrib["protocol"],
                    "state": port.find("state").attrib["state"],
                    "service": {
                        "name": port.find("service").attrib.get("name", ""),
                        "product": port.find("service").attrib.get("product", ""),
                        "version": port.find("service").attrib.get("version", "")
                    } if port.find("service") is not None else {}
                }
                host_info["ports"].append(port_info)

            result = {
                "target": self.target,
                "scanned_at": datetime.utcnow().isoformat(),
                "nmap": [host_info]
            }

        except Exception as e:
            result = {"error": str(e)}

        Path("data_test").mkdir(exist_ok=True)
        path = Path("data_test") / (self.target.replace(".", "_") + "_nmap.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

        return result

