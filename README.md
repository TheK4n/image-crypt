

<h1 align="center">ImageCrypt</h1>

<p align="center">
  <a href="https://github.com/TheK4n">
    <img src="https://img.shields.io/github/followers/TheK4n?label=Follow&style=social">
  </a>
  <a href="https://github.com/TheK4n/ImageCrypt">
    <img src="https://img.shields.io/github/stars/TheK4n/ImageCrypt?style=social">
  </a>
</p>

* [Project description](#chapter-0)
* [Installation](#chapter-1)
* [Usage](#chapter-2)
* [FAQ](#chapter-3)


<a id="chapter-0"></a>
## Project description 

[Project](https://github.com/AlexGyver/crypto) [AlexGyver](https://github.com/AlexGyver) on Python by [TheK4n](https://github.com/TheK4n)
\
_Design by [Пашушка](https://github.com/PAPASKAS)_

\
Byte packing in decimal rgb:
```python
this_color = b * 65536 + g * 256 + r
this_char = ord(char)

new_color = (this_color & 0xF80000)       # 11111000 00000000 00000000
new_color |= (this_char & 0xE0) << 11     # 00000111 00000000 00000000
new_color |= (this_color & (0x3F << 10))  # 00000000 11111100 00000000
new_color |= (this_char & 0x18) << 5      # 00000000 00000011 00000000
new_color |= (this_color & (0x1F << 3))   # 00000000 00000000 11111000
new_color |= (this_char & 0x7)            # 00000000 00000000 00000111
```

Unpacking byte:
```python
new_color = b * 65536 + g * 256 + r

this_char = 0
this_char |= (new_color & 0x70000) >> 11  # 00000111 00000000 00000000 -> 00000000 00000000 11100000
this_char |= (new_color & 0x300) >> 5     # 00000000 00000011 00000000 -> 00000000 00000000 00011000
this_char |= (new_color & 0x7)
```

\
Method for russian symbols:
```python
# Encryption
if this_char > 1000:
    this_char -= 890

# Decryption
if this_char > 130:
    this_char += 890
```

<a id="chapter-1"></a>
## Installation:

Clone repository and installing dependencies:

```bash
git clone https://github.com/TheK4n/ImageCrypt.git
cd ImageCrypt
make
```

<a id="chapter-2"></a>
## Usage

### GUI:
```
image-crypt-gui
```
[![Example](src/preview.png)]()



### Bash:

```bash
image-crypt --help
```
**Result**:
```text
usage: image-crypt [-h] (-e | -d) [-o OUTPUT] images [images ...]

Stenography encryption tool

positional arguments:
  images                path to image to encrypt of decrypt

optional arguments:
  -h, --help            show this help message and exit
  -e, --encrypt         encrypts text in image
  -d, --decrypt         decrypts text from image
  -o OUTPUT, --output OUTPUT
                        name of output image
```

\
For **encryption**: 
```bash
image-crypt -e images/test.jpg
```
**Result**: saved image with default name _image_encrypted.bmp_


For **decryption**: 
```bash
image-crypt -d test_encrypted.bmp
```
**Result**: decrypted text

\
**Example:**
```bash
echo "test message" | image-crypt -e image.png -o test_image.bmp

image-crypt -d test_image.bmp > res.txt
```

### Docker:

**Example:**
```bash
docker run --rm -it -v $(pwd):/image-crypt -w /image-crypt image-crypt image-crypt -e image.png
```
Enter the text, press <kbd>Ctrl</kbd> + <kbd>d</kbd> and enter the passphrase

**Result**: Encrypted image in work directory


<a id="chapter-3"></a>
# FAQ

> *Q*: What is the level of cryptographic strength?

> *A*: It uses symmetric and asymmetric encryption methods such as AES and RSA.

<br>

> *Q*: Does it pack the image data into text?

> *A*: No, it's packing text into image pixels.

<h1 align="center"><a href="#top">▲</a></h1>
