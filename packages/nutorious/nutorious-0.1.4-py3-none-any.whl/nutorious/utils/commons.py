def mkstring(xs, sep=""):
    return sep.join(xs)


def print_(a):
    print(a, end="")


def coalsece(*values):
    for v in values:
        if v is not None:
            return v
    return None
