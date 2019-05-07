import cv2
import numpy as np


def getCameraParams():
    """
    Gets the calculated parameters needed for un-distortion
    operation for camera model = elp-usb500w02m 170"
    :return: (DIM, K, D)
    """
    DIM = (640, 480)
    K = np.array([[290.0773533560033, 0.0, 315.8447290199889],
                  [0.0, 289.81788954159555, 237.67840019402686], [0.0, 0.0, 1.0]])
    D = np.array([[-0.04537422043483615], [0.004714232266013175],
                  [-0.01138740537074217], [0.0048864218521344465]])

    return DIM, K, D


def undistort(img):
    """
    Applies fish-eye un-distortion to the given image.
    :param img: is the image matrix.
    :return: undistorted image matrix.
    """
    DIM, K, D = getCameraParams()

    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    return cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
