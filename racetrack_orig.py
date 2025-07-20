import os
import itertools
import json
from pyglet import image


class Track:
    def __init__(self, index):
        self.track_image = image.load(os.path.join("images", f"track{index}.png"))
        self.track_overlay_image = image.load(os.path.join("images", f"track{index}-overlay.png"))

        with open(os.path.join("images", f"track{index}.json"), "r") as file:
            data = json.load(file)

        self.checkpoints = data["checkpoints"]
        pitch = self.track_image.width * len("RGBA")
        pixels = self.track_image.get_data("RGBA", pitch)
        map = [1 if b == (75, 75, 75, 255) else 0 for b in itertools.batched(pixels, 4)]
        self.map_matrix = [map[n : n + self.track_image.width]
                           for n in range(0,
                                          self.track_image.width * self.track_image.height,
                                          self.track_image.width)]
        # print(self.map_matrix[270])


    def is_road(self, x, y):
        if x < 0 or x > 960 or y < 0 or y > 540:    # x and y out of bounds always returns False
            return False

        return self.map_matrix[int(y)][int(x)] == 1
