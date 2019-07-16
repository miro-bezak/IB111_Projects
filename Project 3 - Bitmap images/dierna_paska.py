# -*- coding: UTF-8 -*-
"""FI MUNI Brno - IB111: Basics of Programming, Advanced Group
-Project 3b: Bitmap graphics - decoding Punched tape into ASCII.
Author: Miroslav Bezák, 485221
"""
from PIL import Image


def print_pixels(image: Image) -> None:
    """Prints out the pixels, displaying a cut-out with a 1,
    a non-cut-out with 0."""
    for y_coord in range(image.height):
        for x_coord in range(image.width):
            print(int(image.getpixel((x_coord, y_coord)) == 255), end=" ")
        print()


def crop_and_bilevel(image: Image) -> Image:
    """Crops the image into a smaller rectangle to allow easier searching
    and converts into bilevel(black & white)."""
    image = image.convert(mode="1")
    image = image.crop(box=(61, 7, 145, 115))
    return image


def convert_to_array(image: Image) -> list:
    """Takes out the pixel DATA from the Image object and converts them into
    a list."""
    pixels = []
    for y_coord in range(image.height):
        row = []
        for x_coord in range(image.width):
            row.append(int(image.getpixel((x_coord, y_coord)) == 255))
        pixels.append(row)

    return pixels


def find_holes(pixels: list) -> list:
    """Finds the holes in the punched tape and returns them as a list of
    tuples representing their coordinates in the image."""
    holes = []  # list of (x_coord,y_coord) tuples
    # A hole (a binary 1 on the punched tape) is easily recognizable as a
    # sequence of eight ones in the list representation of the image.
    eight_ones = [1, 1, 1, 1, 1, 1, 1, 1]
    for y_coord, _ in enumerate(pixels):
        for x_coord in range(len(pixels[0]) - 8):
            next_pixels = pixels[y_coord][x_coord:x_coord + 8]
            if next_pixels == eight_ones \
                    and pixels[y_coord - 1][x_coord:x_coord + 8] != eight_ones:
                holes.append((x_coord, y_coord))

    return holes


def evaluate_holes(holes: list) -> dict:
    """Evaluates the positions of the holes according to their position in
    the image to distribute them into rows and columns where each row
    represents one binary number."""
    rows = {}  # keys are exponents (2^key)
    row_to_exponent = {'2': 6, '3': 5, '4': 4, '5': 3, '7': 2, '8': 1, '9': 0}
    for hole in holes:
        column_number = hole[0] // 10
        column_number = column_number + 1 if column_number == 2 \
            else column_number
        row_number = hole[1] // 10
        exponent = str(row_to_exponent[str(row_number)])
        if exponent in rows.keys():
            rows[exponent].append(column_number)
        else:
            rows[exponent] = [column_number]
    return rows


def evaluate_ascii(rows: dict) -> None:
    """Coverts the binary numbers into ASCII characters."""
    chars = {'3': 0, '4': 0, '5': 0, '6': 0, '7': 0}
    for key in rows.keys():
        for i in range(len(rows[key])):
            chars[str(rows[key][i])] += 2 ** (int(key))

    for char in chars:
        chars[char] = chars[char], chr(chars[char])

    for char in chars:
        print(chars[char][1], end="")


IMG = Image.open("img10_ascii.png")

IMG = crop_and_bilevel(IMG)
DATA = convert_to_array(IMG)
CUT_OUTS = find_holes(DATA)
EXPONENT_DATA = evaluate_holes(CUT_OUTS)

evaluate_ascii(EXPONENT_DATA)
