import ast
import os.path
from random import seed, randint
from hashlib import sha512, scrypt
from PIL import Image, ImageDraw
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA
import os


__all__ = ['CryptImageSave', 'MoreThanImgError', 'WrongImage']


class MoreThanImgError(Exception):
    pass


class WrongImage(Exception):
    pass


def get_sha512(passwd: str) -> str:
    return sha512(passwd.encode()).hexdigest()


class Pixel:

    def __init__(self, color: (int, int, int)):

        if not isinstance(color, tuple) or len(color) < 3:
            raise WrongImage
        self.__color = color

    @staticmethod
    def __get_encrypted_color(this_color: int, char: int) -> int:
        this_char = char
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
    def __get_decrypted_char(new_color: int) -> int:

        this_char = 0
        this_char |= (new_color & 0x70000) >> 11  # 00000111 00000000 00000000 -> 00000000 00000000 11100000
        this_char |= (new_color & 0x300) >> 5  # 00000000 00000011 00000000 -> 00000000 00000000 00011000
        this_char |= (new_color & 0x7)

        if this_char > 130:
            this_char += 890

        return this_char

    def __rgb_to_dec(self):
        """Возвращает число, переводит RGB в десятичный формат"""
        r, g, b = self.__color[:3]
        return b * 65536 + g * 256 + r

    def encrypt(self, char: int):
        return self.__get_encrypted_color(self.__rgb_to_dec(), char)

    def decrypt(self):
        return self.__get_decrypted_char(self.__rgb_to_dec())


class Text:
    def __init__(self, text: str):
        self.__text = text

    def __parse_hash(self, block_size=24) -> tuple:

        return tuple(map(b64decode, (self.__text[:block_size], self.__text[block_size:block_size * 2],
                                     self.__text[block_size * 2:block_size * 3], self.__text[block_size * 3:])))

    def encrypt(self, key: str):
        salt = get_random_bytes(AES.block_size)
        private_key = scrypt(
            key.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
        cipher_config = AES.new(private_key, AES.MODE_GCM)
        cipher_text, tag = cipher_config.encrypt_and_digest(self.__text.encode('utf-8'))
        self.__text = "".join(map(lambda x: b64encode(x).decode("utf-8"), (salt, cipher_config.nonce, tag, cipher_text)))
        return self

    def decrypt(self, key: str):
        salt, nonce, tag, cipher_text = self.__parse_hash()
        private_key = scrypt(
            key.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
        cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
        self.__text = cipher.decrypt_and_verify(cipher_text, tag).decode('utf-8')
        return self

    def encrypt_rsa(self, pub_key):

        pub = RSA.importKey(open(pub_key).read())
        encryptor = PKCS1_OAEP.new(pub)

        self.__text = str(encryptor.encrypt(self.__text.encode()))
        return self

    def decrypt_rsa(self, priv_key):
        priv = RSA.importKey(open(priv_key).read())
        decryptor = PKCS1_OAEP.new(priv)
        self.__text = decryptor.decrypt(ast.literal_eval(str(self.__text)))
        return self

    def get(self) -> str:
        return self.__text


class ImageBase:
    def __init__(self, image_path: str):
        self.__image_path = image_path

        self.__img = Image.open(self.__image_path)
        self.__size = self.get_size()
        self.__pix = self.__img.load()  # пиксели

    def get_size(self):
        return self.__img.size[0] * self.__img.size[1]

    def __gen_coords(self):
        width, height = self.__img.size
        width -= 1
        height -= 1
        while True:
            yield randint(0, width), randint(0, height)

    def encrypt(self, msg: str, key: str) -> Image:
        msg += '\0'
        if len(msg) > self.__size:
            raise MoreThanImgError(f'Length of message <{len(msg)}> more than image <{self.__size}>')

        img_new = ImageDraw.Draw(self.__img)

        checked = []
        gen_msg = (i for i in msg.encode())  # генератор
        seed(get_sha512(key))
        n = 0  # счетчик
        for i in self.__gen_coords():

            if n >= len(msg):  # если кол-во записанных больше или равно длине сообщения - конец цикла
                break
            if i in checked:  # если координаты уже были использованы
                continue  # пропустить цикл
            else:
                try:
                    char = next(gen_msg)
                except StopIteration:
                    break

                p = Pixel(self.__pix[i])

                img_new.point(i, p.encrypt(char))
                n += 1
                checked.append(i)

        seed()  # возвращает зерно рандомизатора в None
        return self.__img

    def decrypt(self, key: str) -> str:

        checked = []
        msg = []
        seed(get_sha512(key))
        n = 0
        for i in self.__gen_coords():
            if n >= self.__size:
                break
            p = Pixel(self.__pix[i])
            char = p.decrypt()
            n += 1
            if chr(char) == '\0':  # завершает цикл когда дошел до метки
                break

            if i in checked:
                continue

            else:
                checked.append(i)
                msg.append(char)
        print(msg)
        seed()  # возвращает зерно рандомизатора в None
        return ''.join(map(chr, msg))


class CryptImageSave:

    def __init__(self, image_path: str):
        self.__image_path = image_path

    @staticmethod
    def _get_filename_without_extension(filename: str) -> str:
        return '.'.join(os.path.basename(filename).split('.')[:-1])

    def save_encrypted_image_gui(self, msg: str, key: str):
        encrypted_image_path = os.path.join(os.path.dirname(self.__image_path),
                                            f'{self._get_filename_without_extension(self.__image_path)}_encrypted.bmp')

        # saves encrypted image in source image directory

        img = ImageBase(self.__image_path)
        t = Text(msg).encrypt(key).get().strip()
        img.encrypt(t, key).save(encrypted_image_path, 'BMP')

    def save_encrypted_image_bash(self, msg, key, new_name=None):

        if new_name is None:
            new_name = self._get_filename_without_extension(self.__image_path) + '_encrypted.bmp'

        # saves encrypted image in work directory

        img = ImageBase(self.__image_path)
        t = Text(msg).encrypt(key).get().strip()
        img.encrypt(t, key).save(new_name, 'BMP')
        return new_name

    def save_encrypted_image_rsa_gui(self, msg: str, key: str):
        encrypted_image_path = os.path.join(os.path.dirname(self.__image_path),
                                            f'{self._get_filename_without_extension(self.__image_path)}_encrypted.bmp')

        # saves encrypted image in source image directory

        img = ImageBase(self.__image_path)
        t = Text(msg).encrypt_rsa(key).get()
        img.encrypt(t, key).save(encrypted_image_path, 'BMP')

    def save_encrypted_image_rsa_bash(self, msg, key, new_name=None):

        if new_name is None:
            new_name = self._get_filename_without_extension(self.__image_path) + '_encrypted.bmp'

        # saves encrypted image in work directory

        img = ImageBase(self.__image_path)
        t = Text(msg).encrypt_rsa(key).get()
        img.encrypt(t, key).save(new_name, 'BMP')
        return new_name

    def get_msg_from_image(self, key: str) -> str:
        img = ImageBase(self.__image_path)
        return Text(img.decrypt(key)).decrypt(key).get().strip()

    def get_msg_rsa(self, key) -> str:
        img = ImageBase(self.__image_path)
        return Text(img.decrypt(key)).decrypt_rsa(key).get().strip()
