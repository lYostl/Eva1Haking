import requests
from datetime import datetime
from pathlib import Path
import json

class GoogleDorksScanner:
    def __init__(self, api_key, search_engine_id):
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.url = "https://www.googleapis.com/customsearch/v1"

    def search(self, query):
        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query
        }

        try:
            response = requests.get(self.url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            items = data.get("items", [])
        except Exception as e:
            items = [{"error": str(e)}]

        results = {
            "query": query,
            "searched_at": datetime.utcnow().isoformat(),
            "results": items
        }

        Path("data_test").mkdir(exist_ok=True)
        filename = query.replace(" ", "_").replace(":", "") + "_dorks.json"
        path = Path("data_test") / filename

        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)

        return results
