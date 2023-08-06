try:
    import dxcam
    from ninja_tools.bbox import BBOX
except ImportError:
    raise 'pip install ninjatools[all]  to use fast capture!'


class FastCapture:
    """A class for fast image capture using the dxcam library."""

    def __init__(self, color="BGR"):
        """
        Initialize the FastCapture object with the specified color format.

        Args:
            color (str): The color format for the captured images (default: "BGR").
        """
        self.camera = dxcam.create(output_color=color)
        self.last_image = None

    def capture(self, bbox: BBOX = None):
        """
        Capture an image using the dxcam library. Optionally, capture a specific region
        of the image defined by a BBOX object.

        Args:
            bbox (BBOX): A BBOX object defining the region to capture (default: None).

        Returns:
            The captured image or the last captured image if the current capture fails.
        """
        image = self.camera.grab(region=bbox() if bbox else None)

        if image is not None:
            self.last_image = image

        return self.last_image
