# Adafruit NeoPixel flame simulator

Tested with the [Adafruit NeoPixel LED strip](https://www.adafruit.com/product/1461?length=1).

Based on the algorithm from http://pastebin.com/xYEpxqgq


## Setup 

[Wire the NeoPixel LEDs to the Raspberry Pi](https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring) as desired. Right now it expects the NeoPixel DIN to be connected to GPIO pin 18.

```shell
pip install git+https://github.com/willbarton/neopixelflames
sudo neopixelflames
```

You should then see a red-ish "heat" glow with occasional yellow/white "sparking" that affects adjacent pixels.

## Config

You can specify a JSON configuration file, if you want to change the defaults:

```
sudo neopixelflames -c config.json
```

The config values of interest are:

- `num_pixel`: the number of pixels available
- `sparking`: The chance (out of 255) that a new spark will be lit each iteration
- `cooling`: How much does the fire cools (out of 100) with each iteration
- `colors`: RGB values listed from coolest color to hottest color
- `levels`: RGB color balance

Some ideas:

- Default, cool embers:

   ```json
   {
       "num_pixels": 60,
       "sparking": 100,
       "cooling": 50,
       "colors": [
           [0.75, 0.0, 0.2],
           [1.0, 0.0, 0.0],
           [1.0, 0.5, 0.0],
           [1.0, 0.7, 0.2],
           [1.0, 0.9, 0.9]
       ],
       "levels": [0.9, 1.0, 0.15]
   }
   ```


- Goblet of fire:

   ```json
   {
       "num_pixels": 60,
       "sparking": 100,
       "cooling": 50,
       "colors": [
           [0.2, 0.34, 0.83],
           [0.36, 0.52, 0.95],
           [0.5, 0.85, 0.98],
           [0.73, 0.97, 0.98],
           [0.9, 0.9, 1.0]
       ],
       "levels": [0.9, 1.0, 0.15]
   }
   ```

- 'Merica:
   
   ```json
   {
       "num_pixels": 60,
       "sparking": 100,
       "cooling": 50,
       "colors": [
           [0.0, 0.0, 0.98],
           [1.0, 0.0, 0.09],
           [1.0, 1.0, 1.0],
       ],
       "levels": [0.9, 1.0, 0.15]
   }
   ```

- Pride:

   ```json
   {
       "num_pixels": 60,
       "sparking": 100,
       "cooling": 50,
       "colors": [
           [0.52, 0.0, 0.49],
           [0.0, 0.0, 0.98],
           [0.0, 0.5, 0.09],
           [1.0, 1.0, 0.25],
           [1.0, 0.65, 0.17],
           [1.0, 0.0, 0.09]
       ],
       "levels": [0.9, 1.0, 0.15]
   }
   ```
