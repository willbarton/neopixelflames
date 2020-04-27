import argparse
import fcntl
import json
import os
import random
import signal
import sys

import board
from colour import Color
import neopixel

import adafruit_fancyled.adafruit_fancyled as fancy


# Basic black body color palette
HEAT_COLORS = [
    (0.75, 0.0, 0.2),  # NCS Red
    (1.0, 0.0, 0.0),   # Red
    (1.0, 0.5, 0.0),   # Orange
    (1.0, 0.7, 0.2),   # Saffron
    (1.0, 0.9, 0.9),   # White
]


# Color balance / brightness for gamma function
LEVELS = (0.9, 1.0, 0.15)


# Default JSON config
DEFAULT_CONFIG = {
    'num_pixels': 60,
    'sparking': 100,
    'cooling': 50,
    'colors': HEAT_COLORS,
    'levels': LEVELS,
    'color_smoothing': False,
}


class NeoPixelFlames(object):

    def __init__(self, pin=None, num_pixels=60, sparking=100, cooling=50,
                 colors=HEAT_COLORS, levels=LEVELS):
    def __init__(self, pin=None, num_pixels=0, sparking=0, cooling=0,
                 colors=HEAT_COLORS, levels=LEVELS, color_smoothing=False):
        # The GPIO pin the pixels are attached to
        if pin is None:
            pin = board.D18
        self.pin = pin

        # The number of pixels available
        self.num_pixels = num_pixels

        # Sparking: What chance (out of 255) is there that a new spark
        # will be lit?
        # Higher chance = more roaring fire.  Lower chance = more flickery fire
        # Suggested range 50-200.
        self.sparking = sparking

        # Cooling: How much does the air cool as it rises?
        # Less cooling = taller flames.  More cooling = shorter flames.
        # Suggested range 20-100
        self.cooling = cooling

        if color_smoothing:
            colors = self.rgb_color_gradient(colors)
        self.colors = [fancy.CRGB(*c) for c in colors]

        # Custom levels
        if levels is not None:
            self.levels = levels

        # Current "heat" value for each pixel
        self.heat_values = [0] * self.num_pixels

        # The pixels themselves
        self.pixels = neopixel.NeoPixel(
            self.pin,
            self.num_pixels,
            brightness=1.0,
            auto_write=False,
        )

        self.range = list(range(self.num_pixels))

    def rgb_color_gradient(self, colors):
        # Take the colors we were given and calculate a gradient between them
        color_objs = []
        for current_color, next_color in zip(colors, colors[1:]+[None]):
            if next_color is None:
                break
            color_objs += Color(rgb=current_color).range_to(
                Color(rgb=next_color), 10
            )

        return (c.rgb for c in color_objs)

    def cool(self):
        """ Cool down every cell a little """
        for p in range(self.num_pixels):
            self.heat_values[p] = max(
                0,
                self.heat_values[p] -
                random.uniform(0, ((self.cooling * 10) / self.num_pixels) + 2)
            )

    def heat(self):
        """ Heat from each cell drifts 'up' and diffuses a little """
        for p in reversed(range(1, self.num_pixels)):
            self.heat_values[p] = (
                (
                    self.heat_values[p - 1] +
                    self.heat_values[p - 2] +
                    self.heat_values[p - 2]
                ) / 3
            )

    def spark(self):
        """ Randomly ignite new 'sparks' of heat near the bottom """
        if random.randint(0, 255) < self.sparking:
            p = random.randint(0, int(self.num_pixels / 2))
            self.heat_values[p] = (
                self.heat_values[p] + random.uniform(160, 240)
            )

    def set_pixel_values(self):
        """ Set the pixels to the current heat values """
        random.shuffle(self.range)
        for p in self.range:
            color_index = self.heat_values[p] / 240
            color = fancy.palette_lookup(self.colors, color_index)
            color = fancy.gamma_adjust(color, brightness=self.levels)
            self.pixels[p] = color.pack()

    def __iter__(self):
        return self

    def __next__(self):
        self.cool()
        self.heat()
        self.spark()
        self.set_pixel_values()
        self.pixels.show()

    def reset(self):
        for p in range(self.num_pixels):
            self.pixels[p] = (0, 0, 0)
        self.pixels.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--config-file", help="path to json config file"
    )
    args = parser.parse_args()

    if args.config_file:
        with open(args.config_file, 'r') as json_file:
            config = json.load(json_file)
    else:
        config = DEFAULT_CONFIG

    fire = NeoPixelFlames(
        num_pixels=config['num_pixels'],
        sparking=config['sparking'],
        cooling=config['cooling'],
        colors=config['colors'],
        levels=config['levels'],
        color_smoothing=config['color_smoothing'],
    )

    def signal_handler(signal, frame):
        fire.reset()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while True:
        next(fire)


if __name__ == '__main__':
    main()
