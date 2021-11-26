import os.path
from random import seed, randint
from hashlib import sha512, scrypt
from PIL import Image, ImageDraw
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
import os
from Cryptodome.Random import get_random_bytes

__all__ = ['CryptImageSave', 'MoreThanImgError']


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

    @staticmethod
    def __get_sha512(passwd: str) -> str:
        return sha512(passwd.encode()).hexdigest()

    @staticmethod
    def __get_encrypted_text_aes(text: str, key: str) -> str:
        salt = get_random_bytes(AES.block_size)

        private_key = scrypt(
            key.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)

        cipher_config = AES.new(private_key, AES.MODE_GCM)

        cipher_text, tag = cipher_config.encrypt_and_digest(text.encode('utf-8'))

        return f"{b64encode(salt).decode('utf-8')}" \
               f"{b64encode(cipher_config.nonce).decode('utf-8')}" \
               f"{b64encode(tag).decode('utf-8')}" \
               f"{b64encode(cipher_text).decode('utf-8')}"

    @staticmethod
    def __parse_hash(encrypted_text: str, block_size=24) -> tuple:

        return tuple(map(b64decode, (encrypted_text[:block_size], encrypted_text[block_size:block_size * 2],
                                     encrypted_text[block_size * 2:block_size * 3], encrypted_text[block_size * 3:])))

    def __get_decrypted_text_aes(self, hashed_text: str, key: str) -> str:
        salt, nonce, tag, cipher_text = self.__parse_hash(hashed_text)

        private_key = scrypt(
            key.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)

        cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

        return cipher.decrypt_and_verify(cipher_text, tag).decode('utf-8')

    def _encrypt(self, image_name: str, msg: str, key: str) -> Image:

        msg = self.__get_encrypted_text_aes(msg, key)


        msg += '\0'  # добавляет в конец сообщения как метку

        img = Image.open(image_name)
        pix = img.load()  # пиксели
        img_new = ImageDraw.Draw(img)

        size = img.size[0] * img.size[1]
        if len(msg) > size:
            raise MoreThanImgError(f'Length of message <{len(msg)}> more than image <{size}>')

        checked = []
        gen_msg = (i for i in msg)  # генератор
        seed(self.__get_sha512(key))
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
        seed(self.__get_sha512(key))
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
        return self.__get_decrypted_text_aes(msg, key)


class CryptImageSave(CryptImage):

    def __init__(self, image_path: str):
        self.__image_path = image_path

    @staticmethod
    def _get_filename_without_extension(filename: str) -> str:
        return '.'.join(os.path.basename(filename).split('.')[:-1])

    def save_encrypted_image_gui(self, msg: str, key: str):
        encrypted_image_path = os.path.join(os.path.dirname(self.__image_path),
                                            f'{self._get_filename_without_extension(self.__image_path)}_encrypted.bmp')

        # saves encrypted image in source image directory
        self._encrypt(self.__image_path, msg, key).save(encrypted_image_path, 'BMP')

    def save_encrypted_image_bash(self, msg, key, new_name=None):

        if new_name is None:
            new_name = self._get_filename_without_extension(self.__image_path) + '_encrypted.bmp'

        # saves encrypted image in work directory
        self._encrypt(self.__image_path, msg, key).save(new_name, 'BMP')
        return new_name

    def get_msg_from_image(self, key: str) -> str:
        return self._decrypt(self.__image_path, key).strip()


def main():
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        crc = CryptImageSave('')
        crc._encrypt('../images/test4k.jpg', 'message', 'key').save('res.bmp', 'BMP')

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()


if __name__ == '__main__':
    main()
