import re
from urllib.parse import urlparse


def get_id_from_url(url: str, split_on="/", index_num=-2):
    url_id = None
    if isinstance(url, str) and split_on in url:
        split_url = url.split(split_on)
        url_id = split_url[index_num]
    return url_id


def get_post_id_from_li_url(li_url):
    if len(li_url) <= 0:
        return li_url
    if "?" in li_url:
        li_url = li_url.split("?")[0]
    if li_url[-1] == "/":
        li_url = li_url[:-1]
    return li_url.split("/")[-1]


def is_valid_premise_url(url):
    if not isinstance(url, str):
        return False
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return False
    if parsed_url.netloc != "app.copyfactory.io":
        return False
    if "premises" not in parsed_url.path:
        return False
    return True


def fix_website(site):
    if not isinstance(site, str):
        site = ""
    site = re.search(r"[\w\.\-]+\.[a-z0-9]*[a-z][a-z0-9]*(?:/[\w\.\-/]*)?", site)
    if site:
        site = site.group(0)
        if "https://" not in site:
            site = f"https://{site}"
    return site


def is_google_workflow_url_valid(url):
    """
    Check that url is a url and that its a google spreadsheet.
    """
    if not isinstance(url, str):
        return False
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return False
    if parsed_url.netloc != "docs.google.com":
        return False
    if "spreadsheets" not in parsed_url.path:
        return False
    return True


def find_item(obj: dict, key: str):
    """
    Recursive search through an object to find key
    """
    if key in obj:
        return obj[key]
    for k, v in obj.items():
        if isinstance(v, list):
            for l_item in v:
                i = find_item(l_item, key)
                if i is not None:
                    return i
        if isinstance(v, dict):
            item = find_item(v, key)
            if item is not None:
                return item


def replace_keys(dictionary: dict, mapping: dict) -> dict:
    """
    Go through original object and swap any keys to the target mapping.
    """
    if not isinstance(dictionary, dict) and not isinstance(mapping, dict):
        return dictionary
    empty = {}
    # special case when it is called for element of array being NOT a dictionary
    if isinstance(dictionary, str):
        # nothing to do
        return dictionary

    for k, v in dictionary.items():
        if isinstance(v, dict):
            empty[mapping.get(k, k)] = replace_keys(v, mapping)
        elif isinstance(v, list):
            newvalues = [replace_keys(x, mapping) for x in v]
            empty[mapping.get(k, k)] = newvalues
        else:
            empty[mapping.get(k, k)] = v
    return empty
