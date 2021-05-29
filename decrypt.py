import sys
from source.Crypto import *

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('[X] Use python decrypt.py <image_name> <key>')
        sys.exit(-1)

    for i in sys.argv:
        if not isinstance(i, str):
            print('[X] All arguments must be string!')
            sys.exit(-1)

    print('[*] Result:', decrypt(sys.argv[1], sys.argv[2]))
    sys.exit(1)
