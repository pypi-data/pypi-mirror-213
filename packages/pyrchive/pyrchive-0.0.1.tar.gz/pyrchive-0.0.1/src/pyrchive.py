import requests
from bs4 import BeautifulSoup
import time
import urllib.parse


class ArchiveSesh:
    def __init__(self):
        self.submit_id = self._fetch_submit_id()

    def _fetch_submit_id(self):
        url = "https://archive.is"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Request to {url} failed with status: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        submit_id_element = soup.find("input", {"name": "submitid"})

        if submit_id_element is None or "value" not in submit_id_element.attrs:
            raise Exception("submitid value not found")

        return submit_id_element["value"]

    def archive_url(self, url):
        encoded_submit_id = urllib.parse.quote(self.submit_id)
        encoded_url = urllib.parse.quote(url)
        archive_url = f"https://archive.is/submit/?submitid={encoded_submit_id}&url={encoded_url}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
        }

        response = requests.get(archive_url, headers=headers, timeout=10)
        extracted_url = response.url

        return extracted_url

    def wait_for_archive(self, url, iter_wait=10, max_iter=3):
        iter = 0
        while True:
            archive_url = self.archive_url(url)
            if "submitid" not in archive_url or iter >= max_iter:
                return archive_url
            iter += 1
            print(f"Waiting for next iteration... ({iter} of {max_iter})")
            time.sleep(iter_wait)
