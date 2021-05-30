from os import mkdir
from random import seed, shuffle
from typing import *

from PIL import Image, ImageDraw

try:
    mkdir('../results')
except FileExistsError:
    pass


def get_random_list(length: int, key: Union[int, float, str]) -> list[int]:
    seed(key)
    lst = [i for i in range(length)]
    shuffle(lst)
    seed()
    return lst


def get_matrix(array_: tuple[int, int]) -> list:

    n = 0
    mat = []
    height, width = array_
    for i in range(height):
        lst = []
        for i2 in range(width):
            lst.append(n)
            n += 1
        mat.append(lst)
    return mat


def get_xy(matrix: list, element: int) -> tuple[int, int]:

    height, width = len(matrix), len(matrix[0])
    index_y = element // width
    index_x = matrix[index_y].index(element)

    return index_y, index_x


def rgb_to_dec(rgb: tuple[int, int, int]) -> int:
    r, g, b = rgb
    return b * 65536 + g * 256 + r


def get_encrypted_color(this_color: int, char: str) -> int:
    this_char = ord(char)

    # упаковка в RGB 323
    new_color = (this_color & 0xF80000)       # 11111000 00000000 00000000
    new_color |= (this_char & 0xE0) << 11     # 00000111 00000000 00000000
    new_color |= (this_color & (0x3F << 10))  # 00000000 11111100 00000000
    new_color |= (this_char & 0x18) << 5      # 00000000 00000011 00000000
    new_color |= (this_color & (0x1F << 3))   # 00000000 00000000 11111000
    new_color |= (this_char & 0x7)            # 00000000 00000000 00000111

    return new_color


def get_decrypted_char(new_color: int) -> str:
    this_char = 0

    this_char |= (new_color & 0x70000) >> 11  # 00000111 00000000 00000000 -> 00000000 00000000 11100000
    this_char |= (new_color & 0x300) >> 5     # 00000000 00000011 00000000 -> 00000000 00000000 00011000
    this_char |= (new_color & 0x7)

    return chr(this_char)


def encrypt(image_name: str, msg: str, key: str):

    msg = msg + '\0'

    img = Image.open(image_name)
    pix = img.load()
    img_new = ImageDraw.Draw(img)

    lst = get_random_list(img.size[0]*img.size[1], key)

    matrix = get_matrix(img.size)

    gen_msg = (i for i in msg)
    for i in lst:
        coord = get_xy(matrix, i)
        try:
            img_new.point(coord, get_encrypted_color(rgb_to_dec(pix[coord]), next(gen_msg)))
        except StopIteration:
            break
    img.save('results\\result.bmp', 'BMP')


def decrypt(image_name: str, key: str) -> str:
    img = Image.open(image_name)
    pix = img.load()
    lst = get_random_list(img.size[0]*img.size[1], key)

    matrix = get_matrix(img.size)

    msg = ''
    for i in lst:
        char = get_decrypted_char(rgb_to_dec(pix[get_xy(matrix, i)]))
        if char == '\0':
            break
        msg += char
    return msg
