import sys
from src.Crypto import *

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('[X] Use python encrypt.py <image_name> <message> <key>')
        sys.exit(-1)

    for i in sys.argv:
        if not isinstance(i, str):
            print('[X] All arguments must be string!')
            sys.exit(-1)

    crt = CryptImage_save(sys.argv[1])
    crt.save_encrypted_image(sys.argv[2], sys.argv[3])

    n = len(list(filter(lambda x: x.split('.')[-1] == 'bmp', list(listdir('results')))))
    print(f'[*] Image saved in results as encrypted_{n}.bmp')
    sys.exit(1)  # Выход
