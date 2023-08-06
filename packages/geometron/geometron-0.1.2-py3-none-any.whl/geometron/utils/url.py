import urllib
import codecs
import json
from os.path import sep


def url_to_path(url, exclude_last_part=False):
    """ Converts an url to a path

    Parameters
    ----------
    url: str
        url to convert
    exclude_last_part: bool, default: False
        If True, the part after the last slash in the url is omitted

    Returns
    -------
    str
        encoded path string
    """
    p = [urllib.parse.urlsplit(url).scheme, urllib.parse.urlsplit(url).netloc]
    p += urllib.parse.urlsplit(url).path.split('/')
    q = [codecs.encode(codecs.encode(i, 'utf8'), 'hex').decode('utf-8') for i in p[:-1]]
    if exclude_last_part:
        p = q
    else:
        p = q + [p[-1]]
    p = sep.join(p)
    return p


def path_to_url(p):
    """ Converts an url encoded with url_to_path as a path back to an url

    Parameters:
    ___________
    p: str
        encoded path string to convert

    Returns
    -------
    str
       url string
    """
    p = [codecs.decode(i, 'hex').decode('utf-8') for i in p.split(sep)]
    url = p[0] + '://' + p[1] + '/'.join(p[2:])
    return url


def http_request(server, data=None):
    request = urllib.request.Request(server, data=urllib.parse.urlencode(data, encoding='utf-8').encode('utf-8'))
    return json.load(url_open_with_retry(request))


def url_open_with_retry(request, timeout=2., retries=3):
    k = 0
    response = None
    while response is None and k < retries:
        try:
            # opens the response
            response = urllib.request.urlopen(request, timeout=timeout)
        except Exception as e:
            print(e)
            response = None
            k += 1
    if response is None:
        print(f'Unable to get response after {k} attempts.')
    return response


def url_request_string(request):
    return f"{request.full_url}{request.data.decode('utf-8')}"
