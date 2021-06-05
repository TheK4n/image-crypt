from os import mkdir, listdir
from random import seed, randint

from PIL import Image, ImageDraw


class MoreThanImgError(Exception):
    pass


try:
    mkdir('../results')
except FileExistsError:
    pass


def gen_coords(size: tuple[int, int]):
    width, height = size
    width -= 1
    height -= 1
    while True:
        yield randint(0, width), randint(0, height)


def rgb_to_dec(rgb: tuple[int, int, int]) -> int:
    """Возвращает число, переводит RGB в десятичный формат"""
    r, g, b = rgb
    return b * 65536 + g * 256 + r


def get_encrypted_color(this_color: int, char: str) -> int:
    this_char = ord(char)
    if this_char > 1000:
        this_char -= 890

    # упаковка в RGB 323
    new_color = (this_color & 0xF80000)  # 11111000 00000000 00000000
    new_color |= (this_char & 0xE0) << 11  # 00000111 00000000 00000000
    new_color |= (this_color & (0x3F << 10))  # 00000000 11111100 00000000
    new_color |= (this_char & 0x18) << 5  # 00000000 00000011 00000000
    new_color |= (this_color & (0x1F << 3))  # 00000000 00000000 11111000
    new_color |= (this_char & 0x7)  # 00000000 00000000 00000111

    return new_color


def get_decrypted_char(new_color: int) -> str:
    this_char = 0
    this_char |= (new_color & 0x70000) >> 11  # 00000111 00000000 00000000 -> 00000000 00000000 11100000
    this_char |= (new_color & 0x300) >> 5  # 00000000 00000011 00000000 -> 00000000 00000000 00011000
    this_char |= (new_color & 0x7)

    if this_char > 130:
        this_char += 890

    return chr(this_char)


def encrypt(image_name: str, msg: str, key: str):
    msg += '\0'  # добавляет в конец сообщения как метку

    img = Image.open(image_name)
    pix = img.load()  # пиксели
    img_new = ImageDraw.Draw(img)

    size = img.size[0] * img.size[1]
    if len(msg) > size:
        raise MoreThanImgError(f'Length of message <{len(msg)}> more than image <{size}>')

    checked = []

    gen_msg = (i for i in msg)  # генератор
    seed(key)
    n = 0  # счетчик
    for i in gen_coords(img.size):

        if n >= len(msg):  # если колво записанных больше или равно длине сообщения - конец цикла
            break
        if i in checked:  # если координаты уже были использованы
            continue  # пропустить цикл
        else:
            try:
                char = next(gen_msg)
            except StopIteration:
                break

            # рисует зашифрованный пиксель
            img_new.point(i, get_encrypted_color(rgb_to_dec(pix[i]), char))
            n += 1
            checked.append(i)

    seed()  # возвращает зерно рандомизатора в None

    # кол-во файлов в формате bmp
    n = len(list(filter(lambda x: x.split('.')[-1] == 'bmp', list(listdir('results')))))
    img.save(f'results\\encrypted_{n + 1}.bmp', 'BMP')  # сохраняет зашифрованную картинку


def decrypt(image_name: str, key: str) -> str:
    img = Image.open(image_name)
    pix = img.load()

    checked = []
    msg = ''
    seed(key)
    n = 0
    for i in gen_coords(img.size):
        if n >= img.size[0] * img.size[1]:
            break
        char = get_decrypted_char(rgb_to_dec(pix[i]))
        n += 1
        if char == '\0':  # завершает цикл когда дошел до метки
            break
        if i in checked:
            continue
        else:
            checked.append(i)
            msg += char

    seed()  # возвращает зерно рандомизатора в None
    return msg
