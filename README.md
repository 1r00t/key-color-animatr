# key-color-animatr
A Python script to animate Logitech keyboard LEDs using an input image.
It maps an image onto the keyboard where each key is a pixel from the image.
Then it walks down the image and creates animation frames.
Output is a .eft file to import in your Logitech Gaming Software.

***Only works for the G810 with German keyboard layout at the moment!***

```bash
# usage: animatr.py [image path] [duration]
python animatr.py path/to/image.jpg 10
```

Here are some example outputs:
[key-color-animatr/tree/master/eft](https://github.com/1r00t/key-color-animatr/tree/master/eft)

* TODO:
    * work on argument parsing
    * add more keyboard layouts
    * add G910 support
    * add more animations
    * figure out why the animation is slow for some images

