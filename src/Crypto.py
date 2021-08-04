from os import mkdir, listdir
from random import seed, randint

from PIL import Image, ImageDraw


class MoreThanImgError(Exception):
    pass


class CryptImage:

    @staticmethod
    def __gen_coords(size: tuple[int, int]):
        width, height = size
        width -= 1
        height -= 1
        while True:
            yield randint(0, width), randint(0, height)

    @staticmethod
    def _rgb_to_dec(rgb: tuple[int, int, int]) -> int:
        """Возвращает число, переводит RGB в десятичный формат"""
        r, g, b = rgb[:3]
        return b * 65536 + g * 256 + r

    @staticmethod
    def _get_encrypted_color(this_color: int, char: str) -> int:
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

    @staticmethod
    def _get_decrypted_char(new_color: int) -> str:
        this_char = 0
        this_char |= (new_color & 0x70000) >> 11  # 00000111 00000000 00000000 -> 00000000 00000000 11100000
        this_char |= (new_color & 0x300) >> 5  # 00000000 00000011 00000000 -> 00000000 00000000 00011000
        this_char |= (new_color & 0x7)

        if this_char > 130:
            this_char += 890

        return chr(this_char)

    def _encrypt(self, image_name: str, msg: str, key: str) -> Image:
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
        for i in self.__gen_coords(img.size):

            if n >= len(msg):  # если кол-во записанных больше или равно длине сообщения - конец цикла
                break
            if i in checked:  # если координаты уже были использованы
                continue  # пропустить цикл
            else:
                try:
                    char = next(gen_msg)
                except StopIteration:
                    break

                # рисует зашифрованный пиксель
                img_new.point(i, self._get_encrypted_color(self._rgb_to_dec(pix[i]), char))
                n += 1
                checked.append(i)

        seed()  # возвращает зерно рандомизатора в None
        return img

    def _decrypt(self, image_name: str, key: str) -> str:
        img = Image.open(image_name)
        pix = img.load()

        checked = []
        msg = ''
        seed(key)
        n = 0
        for i in self.__gen_coords(img.size):
            if n >= img.size[0] * img.size[1]:
                break
            char = self._get_decrypted_char(self._rgb_to_dec(pix[i]))
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


class CryptImageSave(CryptImage):

    def __init__(self, image_name: str):
        self.image_name = image_name

    @staticmethod
    def __make_dir():
        try:
            mkdir('results')
        except FileExistsError:
            pass

    def save_encrypted_image(self, msg: str, key: str):
        self.__make_dir()
        # кол-во файлов в папке с расширением bmp
        n = len(list(filter(lambda x: x.split('.')[-1] == 'bmp', list(listdir('results')))))

        # сохраняет зашифрованную картинку
        self._encrypt(self.image_name, msg, key).save(f'encrypted_{n + 1}.bmp', 'BMP')

    def save_encrypted_image_bash(self, msg, key):
        img_name = '.'.join(self.image_name.split('/')[-1].split('.')[:-1])

        self._encrypt(self.image_name, msg, key).save(f'{img_name}_encrypted.bmp', 'BMP')

    def get_msg_from_image(self, key: str) -> str:
        return self._decrypt(self.image_name, key)
