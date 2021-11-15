di = {
    'image': None,
    'link': 'link'
}
di2 = {
    'image': None,
    'link': 'link'
}
di3 = {
    'image': None,
    'link': None
}

di4 = {
    'image': 'img',
    'link': 'https://scientificrussia.ru/images/y/jvy-full.jpg'
}


def check(cleaned):
    if None in cleaned.values() and all(isinstance(x, type(None)) for x in cleaned.values()) is False:
        return True
    return False


print(check(di))
print(check(di2))
print(check(di3))
print(check(di4))


