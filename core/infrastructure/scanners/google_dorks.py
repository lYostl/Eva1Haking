import os
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout
from dotenv import load_dotenv
import logging
from typing import Optional, List, Dict

# configuración LOG
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

def load_env() -> Optional[Dict[str, str]]:
    load_dotenv()
    api_key = os.getenv("API_KEY")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")

    # Mostrar en consola
    logging.info(f"🔐 API_KEY: {api_key}")
    logging.info(f"🔎 SEARCH_ENGINE_ID: {search_engine_id}")

    if not api_key or not search_engine_id:
        logging.error("❌ API_KEY o SEARCH_ENGINE_ID no encontradas.")
        return None
    return {
        'api_key': api_key,
        'search_engine_id': search_engine_id
    }


def perform_google_search(api_key: str, search_engine_id: str, query: str, start: int = 1, lang: str = 'lang_es') -> Optional[List[Dict]]:
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': query,
        'start': start,
        'lr': lang
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        
        logging.info(f"📤 URL enviada: {response.url}")
        logging.info(f"📥 Status Code: {response.status_code}")
        
        response.raise_for_status()  # esto lanza error si no es 200
        
        data = response.json()

        if 'items' not in data:
            logging.warning("⚠️ No se encontraron resultados en la respuesta.")
            logging.debug(f"Respuesta completa: {data}")

        return data.get('items', [])
        
    except ConnectionError:
        logging.error("🔌 Error de conexión.")
    except Timeout:
        logging.error("⏱️ Timeout alcanzado.")
    except RequestException as e:
        logging.error(f"❗ RequestException: {e}")
        if e.response is not None:
            logging.error(f"📄 Detalle del error: {e.response.text}")
    except Exception as e:
        logging.error(f"🔥 Error inesperado: {e}")

    return None
