from typing import Union, Tuple, List

import cv2
import numpy as np

from ninja_tools.utils import Utilities


class ImageFinder:
    def __init__(self):
        self.u = Utilities()

    def find_image(self, haystack: np.ndarray, needle: np.ndarray, threshold: float = 8,
                   passed_only: bool = True, get_rect: bool = False,
                   get_center: bool = False, get_dist: bool = False,
                   show: bool = False) -> Union[bool, List[Tuple[int, int]]]:
        """
        Finds an image within another image using OpenCV's matchTemplate function.

        Parameters:
            - haystack (np.ndarray): The image to search within.
            - needle (np.ndarray): The image to search for.
            - threshold (float): The minimum match level (0-10) required for a match to be considered a positive result.
            - passed_only (bool): If True, returns a boolean indicating whether a match was found.
                                  If False, returns a list of points where the needle image was found.
            - get_rect (bool): If True, returns a list of rectangles in the form (x, y, x+w, y+h) where the needle
            image was found.
            - get_center (bool): If True, returns a list of points representing the center of the rectangles where
            the needle image was found.
            - get_dist (bool): If True, returns a list of tuples in the form (distance, (x, y)) where distance is the
            distance from the center of the haystack image to the center of the rectangle where the needle image was
            found.
            - show (bool): If True, displays the haystack image with rectangles drawn around the found needles.

        Returns:
            - If passed_only is True, returns a boolean indicating whether a match was found.
            - If passed_only is False, returns a list of points or rectangles where the needle image was found.
        """
        try:
            result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)
            passed = np.amax(result) >= (threshold * 0.1)
            if passed and passed_only:
                return passed

            w_src, h_src = haystack.shape[1], haystack.shape[0]
            w, h = needle.shape[1], needle.shape[0]

            rectangles = []
            points = []

            if get_center or get_rect or show:
                locations = np.where(result >= (threshold * 0.1))
                locations = list(zip(*locations[::-1]))

                if not locations:
                    return False

                for loc in locations:
                    rect = [int(loc[0]), int(loc[1]), w, h]
                    rectangles.append(rect)
                    rectangles.append(rect)

                rectangles, _ = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

                if show:
                    for pt in locations:
                        cv2.rectangle(haystack, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

                print(f"Max match: {np.amax(result):,.2%}")

                cv2.imshow(None, haystack)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()

            for (x, y, w, h) in rectangles:
                if get_rect:
                    points.append((x, y, x + w, y + h))

                else:
                    center_needle = x + int(w / 2), y + int(h / 2)
                    if get_dist:
                        center_haystack = int(w_src / 2), int(h_src / 2)
                        dist = self.u.get_distance(center_haystack, center_needle)
                        points.append((dist, center_needle))

                    else:
                        points.append(center_needle)

            return points

        except Exception as e:
            print(f'An error occurred: {e}')
            return False
