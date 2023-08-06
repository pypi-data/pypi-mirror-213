import numpy as np

def arc_angle_between_point_and_abscissa(p, c):
    """
        Returns the angle of an arc with center c and endpoints at (cx + radius, cy) and (px, py)
        :param p: list of x and y coordinates of a point
        :param c: list of x and y coordinates of the arc center
    """
    theta = np.arctan2(p[1] - c[1], p[0] - c[0])
    return theta + (2 * np.pi if theta < 0 else 0)


def arcCenter(C, iH, oH, iL, oL, diff_radius=None):
    inner_radius = (np.sqrt(np.square(iH.x - C.x) + np.square(iH.y - C.y)) +
                    np.sqrt(np.square(iL.x - C.x) + np.square(iL.y - C.y))) / 2
    if diff_radius:
        outer_radius = inner_radius + diff_radius
    else:
        outer_radius = (np.sqrt(np.square(oH.x - C.x) + np.square(oH.y - C.y)) +
                        np.sqrt(np.square(oL.x - C.x) + np.square(oL.y - C.y))) / 2
    d_inner = [0.5 * abs((iL.x - iH.x)), 0.5 * abs((iH.y - iL.y))]
    d_outer = [0.5 * abs((oL.x - oH.x)), 0.5 * abs((oH.y - oL.y))]
    aa = [np.sqrt(np.square(d_inner[0]) + np.square(d_inner[1])),
          np.sqrt(np.square(d_outer[0]) + np.square(d_outer[1]))]
    bb = [np.sqrt(np.square(inner_radius) - np.square(aa[0])), np.sqrt(np.square(outer_radius) - np.square(aa[1]))]
    if iL.y < iH.y:
        M_inner = [iH.x + d_inner[0], iL.y + d_inner[1]]
        M_outer = [oH.x + d_outer[0], oL.y + d_outer[1]]
        if iL.y >= 0.:
            sign = [-1, -1]
        else:
            sign = [1, 1]
    else:
        M_inner = [iH.x + d_inner[0], iH.y + d_inner[1]]
        M_outer = [oH.x + d_outer[0], oH.y + d_outer[1]]
        if iL.y >= 0.:
            sign = [1, -1]
        else:
            sign = [-1, 1]
    inner = [M_inner[0] + sign[0] * bb[0] * d_inner[1] / aa[0], M_inner[1] + sign[1] * bb[0] * d_inner[0] / aa[0]]
    outer = [M_outer[0] + sign[0] * bb[1] * d_outer[1] / aa[1], M_outer[1] + sign[1] * bb[1] * d_outer[0] / aa[1]]
    return inner, outer