import numpy as np
import math

from matplotlib import pyplot as plt
from matplotlib.lines import Line2D


def arc_angle_between_point_and_abscissa(p, c):
    """
        Returns the angle of an arc with center c and endpoints at (cx + radius, cy) and (px, py)
        :param p: list of x and y coordinates of a point
        :param c: list of x and y coordinates of the arc center
    """
    theta = np.arctan2(p[1] - c[1], p[0] - c[0])
    return theta + (2 * np.pi if theta < 0 else 0)



def find_iH_oH_iL_oL(p1, p2, p3, p4, bore_center):

    point_list = [p1, p2, p3, p4]
    dis1 = math.sqrt((p1[0] - bore_center[0]) ** 2 + (p1[1] - bore_center[1]) ** 2)
    dis2 = math.sqrt((p2[0] - bore_center[0]) ** 2 + (p2[1] - bore_center[1]) ** 2)
    dis3 = math.sqrt((p3[0] - bore_center[0]) ** 2 + (p3[1] - bore_center[1]) ** 2)
    dis4 = math.sqrt((p4[0] - bore_center[0]) ** 2 + (p4[1] - bore_center[1]) ** 2)

    theta1 = arc_angle_between_point_and_abscissa(bore_center, p1)
    theta2 = arc_angle_between_point_and_abscissa(bore_center, p2)
    theta3 = arc_angle_between_point_and_abscissa(bore_center, p3)
    theta4 = arc_angle_between_point_and_abscissa(bore_center, p4)

    theta_list = [theta1, theta2, theta3, theta4]
    distance_list_bore = [dis1, dis2, dis3, dis4]

    theta_array = np.array(theta_list)
    distance_array = np.array(distance_list_bore)
    # Find indices of the two largest values in theta_list

    # Find indices of the two largest values in distance_list_bore
    distance_indices = np.argsort(distance_array)

    # Check the outer points
    high_ind1 = distance_indices[3]
    high_ind2 = distance_indices[2]

    if theta_array[high_ind1] > theta_array[high_ind2]:
        point_oH = point_list[high_ind1]
        point_oL = point_list[high_ind2]
    else:
        point_oH = point_list[high_ind2]
        point_oL = point_list[high_ind1]

    # Check the inner points
    low_ind1 = distance_indices[0]
    low_ind2 = distance_indices[1]
    if theta_array[low_ind1] > theta_array[low_ind2]:
        point_iH = point_list[low_ind1]
        point_iL = point_list[low_ind2]

    else:
        point_iH = point_list[low_ind2]
        point_iL = point_list[low_ind1]

    color = 'k'
    arg = [(point_iH[0], point_iH[1]),
           (point_iL[0], point_iL[1]),
           (point_oH[0], point_oH[1]),
           (point_oL[0], point_oL[1])]

    plt.scatter(arg[0][0],  arg[0][1], color='b')
    plt.text(arg[0][0], arg[0][1], "iH", fontsize=12)

    plt.scatter(arg[1][0],  arg[1][1], color='r')
    plt.text(arg[1][0], arg[1][1], "iL", fontsize=12)

    plt.scatter(arg[2][0],  arg[2][1], color='g')
    plt.scatter(arg[3][0],  arg[3][1], color='y')

    return point_oH, point_oL, point_iH, point_iL