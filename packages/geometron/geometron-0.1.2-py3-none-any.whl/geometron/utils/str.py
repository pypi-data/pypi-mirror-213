import unicodedata


def remove_accents(string):
    """
    Removes unicode accents from a string, downgrading to the base character
    """
    string = ''.join(e for e in string if e.isalnum())
    nfkd = unicodedata.normalize('NFKD', string)
    return u"".join([c for c in nfkd if not unicodedata.combining(c)])
