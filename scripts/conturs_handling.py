def get_rect(conturs):
    # gets rectangle conturs as dict {'xmin', 'ymin', 'xmax', 'ymax'}
    xs, ys = get_xs_or_ys(conturs, 0), get_xs_or_ys(conturs, 1)

    result = {
        'xmin': min(xs),
        'xmax': max(xs),
        'ymin': min(ys),
        'ymax': max(ys),
    }
    return result


def get_xs_or_ys(conturs, typ):
    # typ = 0 => searching for x, 1 => for y
    result = []
    for contur in conturs:
        if isinstance(contur, list):
            result += get_xs_or_ys(contur, typ)
        else:
            result.append(contur[typ])
    return result


def rects_can_not_intersect(rect1, rect2):
    # args are dicts structured like in get_rect function
    return rect1['xmax'] < rect2['xmin'] or \
        rect1['xmin'] > rect2['xmax'] or \
        rect1['ymax'] < rect2['ymin'] or \
        rect1['ymin'] > rect2['ymax']


if __name__ == '__main__':
    print(get_rect([[(1, 2), (3, 4)]]))
    print(get_rect([(1, 2), (3, 4)]))
    print(get_rect([[[(1, 2), (3, 4)]]]))
