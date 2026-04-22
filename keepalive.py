import requests
import time
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

URLS = [
    "https://paisa-circle.preview.emergentagent.com/",
]

INTERVAL_MINUTES = 20
TIMEOUT_SECONDS = 30

def ping(url):
    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        logging.info(f"OK  {url} — {response.status_code} ({response.elapsed.total_seconds():.2f}s)")
    except requests.exceptions.Timeout:
        logging.warning(f"TIMEOUT  {url}")
    except requests.exceptions.ConnectionError:
        logging.error(f"UNREACHABLE  {url}")
    except Exception as e:
        logging.error(f"ERROR  {url} — {e}")

def run():
    import os
    once = os.environ.get("PING_ONCE", "false").lower() == "true"

    if once:
        logging.info("Running in single-ping mode (GitHub Actions).")
        for url in URLS:
            ping(url)
    else:
        logging.info(f"Keepalive started. Pinging every {INTERVAL_MINUTES} min.")
        while True:
            logging.info(f"--- Ping at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC ---")
            for url in URLS:
                ping(url)
            time.sleep(INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    run()
