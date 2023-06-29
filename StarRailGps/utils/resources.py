from pkg_resources import resource_filename


def resource_path(filename):
    return resource_filename('StarRailGps', 'resources/{}'.format(filename))