from copy import deepcopy
from PIL import Image
import argparse
import json
import numpy as np
import os
import random


# get arguments
# TODO: make this good
parser = argparse.ArgumentParser()
parser.add_argument("image")
parser.add_argument("delay")
args = parser.parse_args()
image_path = args.image
delay = args.delay
profile_name, _ = os.path.splitext(os.path.basename(image_path))

# keyboard raster dimensions
# contains "dead" pixel where there is no key
WIDTH, HEIGHT = (22, 7)


def rgb2hex(rgb):
    """
    converts a list of rgb values to hex
    >>> rgb2hex([255, 100, 0])
    #FF6400
    """
    r, g, b = rgb
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def get_key_index(keyboard, key):
    """
    get the x, y postition of a specific key on the keyboard
    """
    for y, row in enumerate(keyboard):
        for x, item in enumerate(row):
            if item == key:
                return (x, y)


# load keyboard layout and base eft template
keyboard_grid_map = json.load(open("template/keygridmap.json", "r"))
base_frame = json.load(open("template/frame.json", "r"))
base_state = json.load(open("template/state.json", "r"))
skeleton = json.load(open("template/skeleton.json", "r"))
skeleton["name"] = profile_name

# load image
im = Image.open(image_path)

# resize image to fit width
wp = (WIDTH / float(im.size[0]))
hz = int((float(im.size[1]) * float(wp)))
im = im.resize((WIDTH, hz), Image.BICUBIC)

# convert to nparray
im = np.array(im)

# walk down the image and populate skeleton
for i in range(im.shape[0] - HEIGHT):
    frame = deepcopy(base_frame)
    state = deepcopy(base_state)

    # basic keys
    for key_id, key_name in state["1"].items():
        x, y = get_key_index(keyboard_grid_map, key_name)
        color = rgb2hex(im[y + i, x])
        state["1"][key_id] = color

    # G logo
    for key_id, key_name in state["10"].items():
        x, y = get_key_index(keyboard_grid_map, key_name)
        color = rgb2hex(im[y + i, x])
        state["10"][key_id] = color

    # music buttons
    for key_id, key_name in state["2"].items():
        x, y = get_key_index(keyboard_grid_map, key_name)
        color = rgb2hex(im[y + i, x])
        state["2"][key_id] = color

    # status LEDs, game mode and light switch
    for key_id, key_name in state["40"].items():
        x, y = get_key_index(keyboard_grid_map, key_name)
        color = rgb2hex(im[y + i, x])
        state["40"][key_id] = color

    frame["index"] = i
    frame["state"] = state
    frame["length"] = delay
    frame["color"] = "#%06x" % random.randint(0, 0xFFFFFF)  # dunno why
    skeleton["transition_list"].append(frame)

# write output to file
json.dump(skeleton, open(f"{profile_name}.eft", "w"), indent=2, sort_keys=True)
