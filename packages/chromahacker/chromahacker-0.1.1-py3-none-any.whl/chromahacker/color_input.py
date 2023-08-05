import numpy as np

def input_color(color_string):
    print(color_string)
    color_string = color_string.lower()
    css_colors = {
        "aliceblue": (240, 248, 255),
        "antiquewhite": (250, 235, 215),
        "aqua": (0, 255, 255),
        "aquamarine": (127, 255, 212),
        "azure": (240, 255, 255),
        "beige": (245, 245, 220),
        "bisque": (255, 228, 196),
    }

    if color_string in css_colors:
        return np.array(css_colors[color_string], dtype=np.uint8)

    if color_string.startswith("#") and len(color_string) == 7:
        print("OK THEN")
        try:
            red = int(color_string[1:3], 16)
            green = int(color_string[3:5], 16)
            blue = int(color_string[5:7], 16)
            return np.array([blue, green, red], dtype=np.uint8)
        except ValueError:
            pass

    return None
