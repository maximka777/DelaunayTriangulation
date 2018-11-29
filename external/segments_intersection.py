def ccw(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])


# Return true if line segments AB and CD intersect
def intersect(a, b, c, d):
    _a = ccw(a, c, d)
    _b = ccw(b, c, d)
    _c = ccw(a, b, c)
    _d = ccw(a, b, d)
    return a != b != c != d and _a != _b and _c != _d
