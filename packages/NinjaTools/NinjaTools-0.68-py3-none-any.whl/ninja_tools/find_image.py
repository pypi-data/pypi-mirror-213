try:
    import cv2
    import numpy as np
except ImportError:
    raise 'pip install ninjatools[image] or ninjatools[all]  to use image functions!'

from ninja_tools.utils import Utilities

u = Utilities()


def find_image(haystack: np.ndarray,
               needle: np.ndarray,
               threshold: float = 8,
               passed_only: bool = True,
               get_rect=False,
               get_center: bool = False,
               get_dist=False,
               show: bool = False):
    result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)
    passed = np.amax(result) >= (threshold * 0.1)

    w_src, h_src = haystack.shape[1], haystack.shape[0]
    w, h = needle.shape[1], needle.shape[0]

    if get_center or get_rect or show:
        locations = np.where(result >= (threshold * 0.1))
        locations = list(zip(*locations[::-1]))

        if not locations:
            return False

        rectangles = []

        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), w, h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, _ = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        points = []

        if show:
            for pt in locations:  # Switch columns and rows
                cv2.rectangle(haystack, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

            print(f"Max match: {np.amax(result):,.2%}")

            cv2.imshow(None, haystack)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()

        # Loop over all the rectangles
        for (x, y, w, h) in rectangles:
            if get_rect:
                points.append((x, y, x + w, y + h))

            else:
                # Determine the center position
                center_needle = x + int(w / 2), y + int(h / 2)

                # Save the points
                if get_dist:  # Gets distance from center
                    center_haystack = int(w_src / 2), int(h_src / 2)
                    dist = u.get_distance(center_haystack, center_needle)
                    points.append((dist, center_needle))

                else:
                    points.append(center_needle)

        return points

    if passed and passed_only:
        return passed

    return False


def load_image(image):
    """
    Load an image given a file path or an image array.

    Args:
        image (Union[str, np.ndarray]): Image path or array.

    Returns:
        np.ndarray: Loaded image.
    """
    if isinstance(image, str):
        return cv2.imread(image, cv2.IMREAD_UNCHANGED)
    return image


def add_alpha_channel(img):
    """
    Add an alpha channel filled with 255 (no transparency) to an image.

    Args:
        img (np.ndarray): Input image.

    Returns:
        np.ndarray: Image with added alpha channel.
    """
    return np.concatenate((img, np.full((*img.shape[:2], 1), 255, dtype=np.uint8)), axis=2)


def find_image2(image, template):
    """
    Find a template in an image and return the maximum confidence value.

    Args:
        image (Union[str, np.ndarray]): Image path or array.
        template (Union[str, np.ndarray]): Template image path or array.

    Returns:
        float: Maximum confidence value.
    """
    img = load_image(image)
    tmpl = load_image(template)

    # Convert input image to 3-channel if it has an alpha channel
    if img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # Add an alpha channel to the template if it doesn't have one
    if tmpl.shape[2] < 4:
        tmpl = add_alpha_channel(tmpl)

    alpha_channel = tmpl[:, :, 3]
    tmpl_rgb = tmpl[:, :, :3]

    # Create a binary mask with the alpha channel
    _, binary_mask = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)

    # Apply the mask to the template
    masked_template = cv2.bitwise_and(tmpl_rgb, tmpl_rgb, mask=binary_mask)

    # Match the template
    result = cv2.matchTemplate(img, masked_template, cv2.TM_CCORR_NORMED, mask=binary_mask)

    # Get the maximum confidence value
    max_confidence = np.max(result)

    return max_confidence
