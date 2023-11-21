from path_prediction import PathPrediction
from calibration import Calibration
from curr_ball_tracking import BallTracking
from arduino_communication import ArduinoCommunication
from setup import Setup
import time

SCREEN_WIDTH =  1920
SCREEN_HEIGHT =  1080

TABLE_WIDTH = 485
TABLE_HEIGHT =  790

# Find all 4 corners
# TO DO - Finding all 4 corners (Brennen)
setup = Setup()
corners = setup.find_corners()
tr = [0,0]
tl = [0,0]
br = [0,0]
bl = [0,0]

# Perform calibration
cal = Calibration(corners[1], corners[0], corners[2], corners[3], TABLE_WIDTH, TABLE_HEIGHT)
cal.find_transformation_matrix()

# While loop: Get pixel value, track path, send value through serial
img_tracking = BallTracking(SCREEN_WIDTH, SCREEN_HEIGHT)
path_prediction = PathPrediction(TABLE_WIDTH, TABLE_HEIGHT)
rpi_communication = ArduinoCommunication()
prev_x, prev_y = 0,0

prev_time = time.time()

while True:
    x, y = img_tracking.get_center()   # TO DO - rename function, bug fixes, return separately (not tuple), color adjustment (Kayal)
    prj = cal.perform_transformation([x,y])
    path_end = path_prediction.find_path_end([prev_x, prev_y], prj)   # TO DO - fix inputs for initializing + function (Enrique)
    # TO DO - smoothing (Enrique)
    # TO DO = get speed to see if it's worth looking at (Brennen)
    path_prediction.check_speed([prev_x, prev_y], prj, time.time()-prev_time)
    prev_x = prj[0]
    prev_y = prj[1]
    rpi_communication.send_msg(str(path_end))
    prev_time = time.time()
