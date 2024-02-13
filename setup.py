import numpy as np
import cv2
import cv2.aruco as aruco


class Setup():
    def __init__(self, screen_width, screen_height, is_video, video_link = ""):
        if is_video:
            self.cap = cv2.VideoCapture(str(video_link))
        else:
            self.cap = cv2.VideoCapture(0, apiPreference=cv2.CAP_ANY, params=[cv2.CAP_PROP_FRAME_WIDTH, screen_width, cv2.CAP_PROP_FRAME_HEIGHT, screen_height])


    def detect_aruco_markers(self):
        ret, im = self.cap.read()

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
        parameters =  aruco.DetectorParameters()
        detector = aruco.ArucoDetector(dictionary, parameters)
        corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
        points = []
        if ids is not None:
            for i in range(len(ids)):
                point_x = int(corners[i][0][0][0])
                point_y = int(corners[i][0][0][1])
                points.append((point_x, point_y, ids[i][0]))

        points = np.array(points)
        sorted_centers = points[points[:,2].argsort()]

        return sorted_centers