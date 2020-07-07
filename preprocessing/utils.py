import shutil
import requests
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def image_download(url, path):
    if os.path.exists(path):
        return

    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    response = session.get(url, stream=True)

    with open(path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


async def async_requester(loop, func, *args):
    await loop.run_in_executor(None, func, *args)
