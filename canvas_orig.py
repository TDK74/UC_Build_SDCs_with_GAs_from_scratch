import random
import time
import math
from pyglet import image
from pyglet.window import Window
from pyglet.window import key
from pyglet.graphics import Batch
from pyglet.sprite import Sprite
from pyglet.shapes import Circle
from pyglet.text import Label
from car import Car
from hud import Hud


class Canvas(Window):
    frame_duration = 1 / 60


    # def __init__(self, track_image_path, cars_image_path):
    def __init__(self, track, cars_image_path):
        super().__init__()
        self.track = track
        self.is_simulating = True
        self.width = 960
        self.height = 540
        self.backgroung_batch = Batch()
        self.cars_batch = Batch()
        self.overlay_batch = Batch()
        # self.track_image_sprite = Sprite(image.load(track_image_path), batch = self.backgroung_batch)
        self.track_image_sprite = Sprite(track.track_image, batch = self.backgroung_batch)
        self.track_overlay_sprite = Sprite(track.track_overlay_image, batch = self.overlay_batch)
        self.car_images = [image.load(car) for car in cars_image_path]
        # self.keyboard = key.KeyStateHandler()   # TODO: remove / comment keyboard control
        # self.push_handlers(self.keyboard)   # TODO: remove / comment keyboard control
        self.checkpoint_sprites = []

        for idx, checkpoint in enumerate(track.checkpoints):
            self.checkpoint_sprites.append((Circle(checkpoint[0], checkpoint[1], 15,
                                                   color = (255, 255, 255, 100),
                                                   batch = self.backgroung_batch),
                                                   Label(str(idx), x = checkpoint[0],
                                                         y = checkpoint[1],
                                                         anchor_x = "center",
                                                         anchor_y = "center",
                                                         color = (255, 255, 255, 255),
                                                         batch = self.backgroung_batch
                                                         )))


    def simulate_generation(self, networks, simulation_round):
        self.car_sprites = []
        self.hud = Hud(simulation_round, networks[0].dimensions, self.overlay_batch)

        for network in networks:
            self.car_sprites.append(Car(network, self.track, random.choice(self.car_images), self.cars_batch))

        self.population_total = len(self.car_sprites)
        self.population_alive = self.population_total
        last_time = time.perf_counter()

        while self.is_simulating and self.population_alive > 0:
            elapsed_time = time.perf_counter() - last_time

            if elapsed_time > self.frame_duration:
                last_time = time.perf_counter()
                self.dispatch_events()
                self.update(elapsed_time)
                self.draw()

        for car in self.car_sprites:
            car.network.highest_checkpoint = car.last_checkpoint_passed
            car.network.smallest_edge_distance = car.smallest_edge_distance

            if car.last_checkpoint_passed == len(self.checkpoint_sprites) - 1:
                car.network.has_reached_goal = True


    def update(self, delta_time):
        for car_sprite in self.car_sprites:
            # car_sprite.update(delta_time, self.keyboard)   # TODO: remove / comment keyboard control
            car_sprite.update(delta_time)

            if car_sprite.is_running:
                if not self.track.is_road(car_sprite.body.x, car_sprite.body.y):
                    car_sprite.shut_off()

                self.check_checkpoints(car_sprite, self.track.checkpoints)

        running_cars = [c for c in self.car_sprites if c.is_running]
        self.population_alive = len(running_cars)

        if self.population_alive > 0:
            self.hud.update(running_cars[0].network, self.population_alive, self.population_total, running_cars[0].speed)


    def draw(self):
        self.clear()
        self.backgroung_batch.draw()
        self.cars_batch.draw()
        self.overlay_batch.draw()
        self.flip()


    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.is_simulating = False
            print("Simulation aborted!")


    def check_checkpoints(self, car_sprite, checkpoints):
        for idx, checkpoint in enumerate(checkpoints):
            length = math.sqrt((checkpoint[0] - car_sprite.body.x) ** 2 +
                               (checkpoint[1] - car_sprite.body.y) ** 2)

            if length < 40:
                car_sprite.hit_checkpoint(idx)
