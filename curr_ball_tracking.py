import cv2
from matplotlib import pyplot as plt
import time
from collections import deque

# Approximate radius of ball in relation to the above dimensions
# Maybe calculate using formula later
BALL_RADIUS = 23

# for the func is_single_color(r, g, b), so that you only have to change it here
DISTINCTIVE_RED = False
DISTINCTIVE_GREEN = True
DISTINCTIVE_BLUE = False

# for the func is_color_rgb(r, g, b), the target color and the amount of wiggle room the color match will have
COLOR_LEEWAY = 50
RED_LEEWAY = COLOR_LEEWAY
GREEN_LEEWAY = COLOR_LEEWAY
BLUE_LEEWAY = COLOR_LEEWAY

BALL_R = 140
BALL_G = 140
BALL_B = 140


class BallTracking():

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

    # If we are looking for the only thing that would have blue in it, for example
    def is_single_color(self, r, g, b):
        # OLD
        # if DISTINCTIVE_RED:
        #     if r >= 128:
        #         return True
        # elif DISTINCTIVE_GREEN:
        #     if g <= 128:
        #         return True
        # elif DISTINCTIVE_BLUE:
        #     if b >= 40:
        #         return True

        # Checks for white ball
        if r >= BALL_R and g >= BALL_G and b >= BALL_B:
            return True
        return False




    def bfs(self, im, start_row, start_col):
        # Define the directions (up, down, left, right)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        # Get the dimensions of the image
        num_rows, num_cols = len(im), len(im[0])
        # Create a 2D array to keep track of visited pixels
        visited = [[False for _ in range(num_cols)] for _ in range(num_rows)]
        # Create a queue for BFS
        queue = deque([(start_row, start_col)])
        # Perform BFS
        total_pixels = 0
        # 35 - 24
        # 25 - 17
        # We know that it will always be short right and down by .68
        # Keep track of the farthest pixels
        max_left = (-1, 100000)
        max_right = (-1, -1)
        max_up = (100000, -1)
        max_down = (-1, -1)
        while queue:
            row, col = queue.popleft()
            # Mark the current pixel as visited
            visited[row][col] = True
            # Process neighbors
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                # Check if the new pixel is within bounds and is of the desired color
                if 0 <= new_row < num_rows and 0 <= new_col < num_cols and not visited[new_row][new_col] and self.is_single_color(im[new_row][new_col][0], im[new_row][new_col][1], im[new_row][new_col][2]):
                    queue.append((new_row, new_col))
                    # Update the furthest left, right, up, and down
                    if max_left[1] > new_col:
                        max_left = (new_row, new_col)
                    if max_right[1] < new_col:
                        max_right = (new_row, new_col)
                    if max_up[0] > new_row:
                        max_up = (new_row, new_col)
                    if max_down[0] < new_row:
                        max_down = (new_row, new_col)
                    visited[new_row][new_col] = True
                    total_pixels += 1

            if total_pixels > 3*BALL_RADIUS and max_right[1]-max_left[1] >= BALL_RADIUS*2/3 and max_down[0]-max_up[0] >= BALL_RADIUS*2/3:

                # print("Ball is ", max_right[1]-max_left[1], " Pixels in Width, and ", max_down[0]-max_up[0], " Pixels in Height")
                # print("Max Left: ", max_left[1], ",", max_left[0])
                # print("Max Right: ", max_right[1], ",", max_right[0])
                # print("Max Up: ", max_up[1], ",", max_up[0])
                # print("Max Down: ", max_down[1], ",", max_down[0])

                center = (max_left[1] + BALL_RADIUS, max_up[0] + BALL_RADIUS)
                # center = find_from_edges(max_left, max_right, max_up, max_down)
                return True, center
        return False, (-1, -1)




    # print(len(im[0]))
    def do_shit(self, im):
        for row in range(0, self.screen_height, BALL_RADIUS):
            for col in range(0, self.screen_width, BALL_RADIUS):
                if self.is_single_color(self.im[row][col][0], self.im[row][col][1], self.im[row][col][2]):
                    top = max(0, row-BALL_RADIUS*4)
                    bottom = min(self.screen_height, row+BALL_RADIUS*4)
                    right = min(self.screen_width, col + BALL_RADIUS*4)
                    left = max(0, col - BALL_RADIUS*4)
                    # cropped_img = 3

                    bfs_true, center = self.bfs(self.im, row, col)
                    if bfs_true:
                        print("Found Color at position: " + str(col) + ", " + str(row))
                        print("Colors at position include " + str(self.im[row][col]))
                        print("Center of ball found at pos (" + str(center[0]) + ", " + str(center[1]) + ")\n\n")
                        return (center)
        return (-1, -1)

    def run(self):
        while True:
            start_time  = time.time()
            cap = cv2.VideoCapture(0)
            ret, im = cap.read()
            # plt.imshow(im)
            # plt.show()
            ceneter = self.do_shit(im)
            print("Time ellapsed 2: " + str(time.time() - start_time))

