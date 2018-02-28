""" This module is made for is_intersect(segment1, segment2) check
see https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
for logics explanation"""


def area(a_x, a_y, b_x, b_y, c_x, c_y):
    return (b_x - a_x) * (c_y - a_y) - (c_x - a_x) * (b_y - a_y)


def is_on_left_or_right(a_x, a_y, b_x, b_y, c_x, c_y):
    return True if area(a_x, a_y, b_x, b_y, c_x, c_y) > 0 else False


def is_collinear(a_x, a_y, b_x, b_y, c_x, c_y):
    return area(a_x, a_y, b_x, b_y, c_x, c_y) == 0


def x_projection(point):
    return point[0], 0


def y_projection(point):
    return (0, point[1])


def is_intersect(segment1, segment2):
    """Returns True if intersect else False
    segment1 = (p1, q1), segment2 = (p2, q2),
    where p1,q1,p2,q2 - points like (x,y)->tuple, where x,y - coordinates"""
    p1, q1, p2, q2 = *segment1, *segment2

    def case1(p1, q1, p2, q2):
        """1. General Case:
        – (p1, q1, p2) and (p1, q1, q2) have different orientations and
        – (p2, q2, p1) and (p2, q2, q1) have different orientations."""
        subcase1 = is_on_left_or_right(*p1, *q1, *p2) ^ \
            is_on_left_or_right(*p1, *q1, *q2)
        if subcase1:
            subcase2 = is_on_left_or_right(*p2, *q2, *p1) ^ \
                is_on_left_or_right(*p2, *q2, *q1)
            if subcase2:
                return True
        return False

    def case2(p1, q1, p2, q2):
        """2. Special Case
        – (p1, q1, p2), (p1, q1, q2), (p2, q2, p1)
        and (p2, q2, q1) are all collinear and
        – the x-projections of (p1, q1) and (p2, q2) intersect via case1
        – the y-projections of (p1, q1) and (p2, q2) intersect via case1"""
        subcase1 = is_collinear(*p1, *q1, *p2) & is_collinear(*p1, *q1, *q2) &\
            is_collinear(*p2, *q2, *p1) & is_collinear(*p2, *q2, *q1)
        if subcase1:
            xp1, xq1, xp2, xq2 = x_projection(p1), x_projection(q1), \
                x_projection(p2), x_projection(q2)
            subcase2 = case1(xp1, xq1, xp2, xq2)
            if subcase2:
                yp1, yq1, yp2, yq2 = y_projection(p1), y_projection(q1), \
                    y_projection(p2), y_projection(q2)
                subcase3 = case1(yp1, yq1, yp2, yq2)
                if subcase3:
                    return True
        return False
    if case1(p1, q1, p2, q2):
        return True
    elif case2(p1, q1, p2, q2):
        return True
    return False


def inside_polygon(x, y, points):
    """
    Return True if a coordinate (x, y) is inside a polygon defined by
    a list of verticies [(x1, y1), (x2, x2), ... , (xN, yN)].

    Reference: http://www.ariel.com.au/a/python-point-int-poly.html
    """
    n = len(points)
    inside = False
    p1x, p1y = points[0]
    for i in range(1, n + 1):
        p2x, p2y = points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


if __name__ == '__main__':
    """ Some Tests: 1st should be False, 2nd should be True, 3rd should be False """
    segment1 = ((1, 1), (10, 1))
    segment2 = ((1, 2), (10, 2))
    print(is_intersect(segment1, segment2))
    segment1 = ((10, 0), (0, 10))
    segment2 = ((0, 0), (10, 10))
    print(is_intersect(segment1, segment2))
    segment1 = ((-5, -5), (0, 0))
    segment2 = ((1, 1), (10, 10))
    print(is_intersect(segment1, segment2))
