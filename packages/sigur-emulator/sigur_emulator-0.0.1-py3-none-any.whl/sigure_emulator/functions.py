from sigure_emulator.sigur_methods import methods_dict
from traceback import format_exc


def create_points_dict(points):
    points_dict = {}
    for point in range(points):
        point = point + 1  # Поскольку начинается итерация с 0
        point_state = create_point(point)
        points_dict[str(point)] = point_state
    return points_dict


def create_point(point):
    point_state = 'APINFO ID {} NAME "GATE-EXIT" ZONEA 0 ZONEB 0 STATE ONLINE_LOCKED OPENED\r\n'.format(point)
    return point_state


def get_method(command):
    try:
        return {'status': True, 'info': methods_dict[command]['method']}
    except KeyError:
        return {'status': False, 'info': format_exc()}
