from dataclasses import dataclass

import numpy as np
from numpy import asarray

import ninja_tools.sort as sort


@dataclass
class Object:
    track_id: int
    distance: float
    target_rect: tuple
    target_center_x: int
    target_center_y: int
    target_xy: tuple
    image_center_x: int
    image_center_y: int
    image_xy: tuple

    def __getitem__(self, key):
        return getattr(self, key)


class Detect:
    def __init__(self, torch, weights, threshold, iou: float = 0.45, force_reload: bool = False, use_sort: bool = True):
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights, force_reload=force_reload)
        self.model = self.model.to(self.device)
        self.model.conf = threshold
        self.model.iou = iou
        self.torch = torch
        self.use_sort = use_sort

        if self.use_sort:
            self.sort_tracker = sort.Sort()  # Create an instance of the Sort class

        # Test dummy image first, this speeds up the first detection
        _ = self.model(np.zeros((50, 50, 3), dtype=np.uint8))

    def detect(self, img) -> list:
        if img is None:
            return []

        results = self.model(img)

        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        img_height, img_width = img.shape[:2]
        image_center_x, image_center_y = int(img_width / 2), int(img_height / 2)

        # Prepare detections for SORT
        detections_for_sort = []
        for i in range(len(labels)):
            x1 = int(cord[i][0] * img_width)
            y1 = int(cord[i][1] * img_height)
            x2 = int(cord[i][2] * img_width)
            y2 = int(cord[i][3] * img_height)
            score = float(cord[i][4])
            detections_for_sort.append([x1, y1, x2, y2, score])

        # Update the tracker with the new detections
        if self.use_sort:
            tracked_objects = self.sort_tracker.update(asarray(detections_for_sort))
        else:
            tracked_objects = asarray(detections_for_sort)

        detected_rectangles = []

        for track in tracked_objects:
            x1, y1, x2, y2 = track.astype(int)[:4]

            if self.use_sort:
                track_id = int(track[-1])
            else:
                track_id = None

            # Get center of x1, y1, x2, y2
            target_center_x = int((x1 + x2) / 2)
            target_center_y = int((y1 + y2) / 2)

            p0 = self.torch.tensor([image_center_x, image_center_y], device=self.device, dtype=self.torch.float)
            p1 = self.torch.tensor([target_center_x, target_center_y], device=self.device, dtype=self.torch.float)

            detected_rectangles.append(
                Object(
                    track_id=track_id,
                    distance=self.torch.linalg.norm(p0 - p1),
                    target_rect=(x1, y1, x2, y2),
                    target_center_x=target_center_x,
                    target_center_y=target_center_y,
                    target_xy=(target_center_x, target_center_y),
                    image_center_x=image_center_x,
                    image_center_y=image_center_y,
                    image_xy=(image_center_x, image_center_y)
                )
            )

        # Sort rects by distance
        if detected_rectangles:
            detected_rectangles.sort(key=lambda x: x.distance)

        return detected_rectangles

# # Example usage:
# detector_with_sort = Detect(torch, "path/to/weights.pth", threshold=0.5, use_sort=True)
# detector_without_sort = Detect(torch, "path/to/weights.pth", threshold
