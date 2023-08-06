from textwrap import wrap

import jinja2
from PIL import Image


def rgba_to_hex(rgba_tuple, alpha=False):
    output = ""
    if rgba_tuple[3] == 0:
        return "transparent"
    if not alpha:
        rgba_tuple = rgba_tuple[:-1]
    for value in rgba_tuple:
        output += format(value, "x").zfill(2)
    return f"#{output}"


def pixel_list_to_sprite(pixel_values, width=5, alpha=False):
    colors = {}
    colors["transparent"] = None
    for pixel in pixel_values:
        colors[rgba_to_hex(pixel, alpha)] = None

    colors_list = list(colors.keys())

    sprite = ""

    for pixel in pixel_values:
        color = colors_list.index(rgba_to_hex(pixel, alpha)) - 1
        if color > 9:
            color = chr(ord("a") + color - 10)
        if color == -1:
            color = "."
        sprite += str(color)

    sprite = wrap(sprite, width)
    sprite = "\n".join(sprite)
    return {"sprite": sprite, "colors": colors}


def image_to_object(
    file, alpha=False, max_colors=10, x=0, y=0, width=None, height=None
):
    if max_colors > 36:
        raise jinja2.exceptions.TemplateError(
            "Image helper function doesn't support more than 36 colors"
        )
    try:
        image = Image.open(file, "r")
    except IOError as err:
        raise jinja2.exceptions.TemplateError(
            f"Unable to read image file\n  {err}"
        )
    # Crop image if needed
    if width:
        right = x + width
    else:
        right = image.size[0]
    if height:
        bottom = y + height
    else:
        bottom = image.size[1]
    image = image.crop((x, y, right, bottom))
    image = image.convert("RGBA")
    result = pixel_list_to_sprite(
        image.getdata(), width=image.size[0], alpha=alpha
    )
    sprite = result["sprite"]
    colors = result["colors"]
    if len(colors) > 10:
        if "." in sprite:
            image = image.quantize(colors=max_colors + 1)
        else:
            image = image.quantize(colors=max_colors)
        image = image.convert("RGBA")
        result = pixel_list_to_sprite(
            image.getdata(), width=image.size[0], alpha=alpha
        )
        sprite = result["sprite"]
        colors = result["colors"]
    if len(colors) > 1:
        colors.pop("transparent", None)
    return f'{" ".join(colors)}\n{sprite}'
