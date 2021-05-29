from os import mkdir
from random import *
from typing import *

from PIL import Image, ImageDraw

try:
    mkdir('../results')
except FileExistsError:
    pass


def get_random_list(length: int, key: Union[int, float, str]) -> list[int]:
    """ """
    seed(key)
    lst = [i for i in range(length)]
    shuffle(lst)
    seed()
    return lst


def get_xy(array_: tuple[int, int], element: int) -> tuple[int, int]:
    height, width = array_
    n = 0
    mat = []
    for i in range(height):
        lst = []
        for i in range(width):
            lst.append(n)
            n += 1
        mat.append(lst)

    index_y = element // width
    index_x = mat[index_y].index(element)

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

    # распаковка из RGB 323 обратно в байт
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

    gen_msg = (i for i in msg)
    for i in lst:
        coord = get_xy(img.size, i)
        try:
            img_new.point(coord, get_encrypted_color(rgb_to_dec(pix[coord]), next(gen_msg)))
        except StopIteration:
            break
    img.save('results\\result.bmp', 'BMP')


def decrypt(image_name: str, key: str) -> str:
    img = Image.open(image_name)
    pix = img.load()
    lst = get_random_list(img.size[0]*img.size[1], key)

    msg = ''
    for i in lst:
        char = get_decrypted_char(rgb_to_dec(pix[get_xy(img.size, i)]))
        if char == '\0':
            break
        msg += char
    return msg
