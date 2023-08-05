import urllib.request


def access_to(url: str):
    # trying to open gfg
    try:
        urllib.request.urlopen(url)
        return True

    # trying to catch exception when internet is not ON.
    except:
        return False
