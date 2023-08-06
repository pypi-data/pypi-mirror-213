import requests

session = requests.Session()


def get(url, retry=3, logger=None, stop=True, **kwargs) -> requests.Response:
    for c in range(retry):
        try:
            r = session.get(url, **kwargs)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as e:
            if logger:
                logger.warning(f'({c+1}/{retry}) {r.status_code} {e}: {url}')
        except requests.exceptions.ConnectionError as e:
            if logger:
                logger.warning(f'({c+1}/{retry}) {r.status_code} {e}: {url}')
        except requests.exceptions.Timeout as e:
            if logger:
                logger.warning(f'({c+1}/{retry}) {r.status_code} {e}: {url}')
        except Exception as e:
            if logger:
                logger.warning(f'({c+1}/{retry}) {r.status_code} {e}: {url}')
    if logger:
        logger.error(f'failed after {retry} retries for GET {url}')
    if stop:
        quit()
    return r


def post(url, retry=3, logger=None, stop=True, **kwargs) -> requests.Response:
    for c in range(retry):
        try:
            r = session.post(url, **kwargs)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as e:
            if logger:
                logger.warning(f'({c+1}/{retry}) {r.status_code} {e}: {url}')
        except requests.exceptions.ConnectionError as e:
            if logger:
                logger.warning(f'({c+1}/{retry}) {r.status_code} {e}: {url}')
        except requests.exceptions.Timeout as e:
            if logger:
                logger.warning(f'({c+1}/{retry}) {r.status_code} {e}: {url}')
        except Exception as e:
            if logger:
                logger.warning(f'({c+1}/{retry}) {r.status_code} {e}: {url}')
    if logger:
        logger.error(f'failed after {retry} retries for POST {url}')
    if stop:
        quit()
    return r


def close():
    session.close()
