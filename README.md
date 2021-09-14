

<h1 align="center">ImageCrypt</h1>

<p align="center">
  <a href="https://github.com/Pendosv">
    <img src="https://img.shields.io/github/followers/Pendosv?label=Follow&style=social">
  </a>
  <a href="https://github.com/Pendosv/ImageCrypt">
    <img src="https://img.shields.io/github/stars/Pendosv/ImageCrypt?style=social">
  </a>
</p>

* [Project description](#chapter-0)
* [Installation](#chapter-1)
* [Usage](#chapter-2)


<a id="chapter-0"></a>
## Project description 

[Project](https://github.com/AlexGyver/crypto) [AlexGyver](https://github.com/AlexGyver) on Python by [Pend0s](https://github.com/Pendosv)
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

Clone repository, install virtual environment and installing dependencies:

```bash
git clone https://github.com/Pendosv/ImageCrypt.git
cd ImageCrypt
virtualenv venv
source venv\Scripts\activate
python3 -m pip install -r requirements.txt
chmod +x image-crypt
sudo ln -s $PWD/image-crypt /usr/bin/image-crypt
```

<a id="chapter-2"></a>
## Usage

### GUI:
```
python3 main.py
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

<a href="#top">Back to top</a>