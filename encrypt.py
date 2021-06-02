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

    encrypt(sys.argv[1], sys.argv[2], sys.argv[3])
    print('[*] Image saved in results as result.bmp')
    sys.exit(1)
